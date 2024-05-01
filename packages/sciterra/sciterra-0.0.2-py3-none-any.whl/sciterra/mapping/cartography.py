"""Functions for manipulating an atlas based on the document embeddings of the abstracts of its publications."""

import bibtexparser
import inspect
import warnings

import numpy as np

from . import topography
from .atlas import Atlas
from .publication import Publication
from ..librarians.librarian import Librarian
from ..vectorization.vectorizer import Vectorizer
from ..vectorization.projection import Projection, merge, get_empty_projection
from ..misc.utils import get_verbose, custom_formatwarning

from typing import Callable, Tuple
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

warnings.formatwarning = custom_formatwarning

##############################################################################
# Helper function
##############################################################################


def batch_cospsi_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Batch-process a pairwise cosine similarity matrix between embeddings.

    In order to avoid memory errors (e.g. bus error, segfaults) resulting from too large arrays, we batch process the construction of the cospsi_matrix.

    Args:
        embeddings: a numpy array of embeddings of shape `(num_pubs, embedding_dim)`

    Returns:
        cosine_similarities: a 2D numpy array of shape `(num_pubs, num_pubs)` representing the pairwise cosine similarity between each embedding
    """
    batch_size = min(1000, len(embeddings))  # Define a batch size

    cosine_similarities = None
    print(
        f"computing cosine similarity for {len(embeddings)} embeddings with batch size {batch_size}."
    )
    for i in tqdm(range(0, len(embeddings), batch_size)):
        # Process batches to compute cosine similarity
        batch = embeddings[i : i + batch_size]
        if cosine_similarities is None:
            cosine_similarities = cosine_similarity(batch, embeddings)
        else:
            cosine_similarities = np.vstack(
                (cosine_similarities, cosine_similarity(batch, embeddings))
            )

    return cosine_similarities


# Helper function for filtering
def pub_has_attributes(
    pub: Publication,
    attributes: list[str],
) -> bool:
    """Return True if a publication has all `attributes`.

    Args:
        attributes: the list of attributes to check are not `None` for each publication from the atlas.
    """
    return pub is not None and all(
        [getattr(pub, attr) is not None for attr in attributes]
    )


def pub_has_fields_of_study(
    pub: Publication,
    fields_of_study: list[str],
) -> bool:
    """Return true if any of `pub.fields_of_study` are in passed `fields_of_study`."""
    return pub is not None and any(
        [field in fields_of_study for field in pub.fields_of_study]
    )


##############################################################################
# Cartographer
##############################################################################


class Cartographer:
    """A basic wrapper for obtaining and updating atlas projections.

    `self.librarian`: the Librarian object used to query a bibliographic database API.
    `self.vectorizer`: the Vectorizer object used to get a document embedding for each abstract
    `self.pubs_per_update`: a list of lists of publication str ids, representing the publications that exist at each time step / expansion update.
    `self.update_history`: an np.array of ints representing when publications were added. A value of -2 indicates no record of being added.
    """

    def __init__(
        self,
        librarian: Librarian = None,
        vectorizer: Vectorizer = None,
    ) -> None:
        self.librarian = librarian
        self.vectorizer = vectorizer

        self.pubs_per_update: list[list[str]] = []
        self.update_history: np.ndarray = None

    ######################################################################
    # Get an Atlas from bibtex
    ######################################################################

    def bibtex_to_atlas(self, bibtex_fp: str, *args, **kwargs) -> Atlas:
        """Convert a bibtex file to an atlas, by parsing each entry for an identifier, and querying an API for publications using `self.librarian`.

        NOTE: the identifiers in the corresponding atlas will be API-specific ids; there is no relationship between the parsed id used to query papers (e.g. 'DOI:XYZ' in the case of SemanticScholar) and the resulting identifier associated with the resulting Publication object, (a paperId, a bibcode, etc.) Therefore, the purpose of using the `bibtex_to_atlas` method is primarily for initializing literature exploration in a human-readable way. If you want to obtain as many publications as identifiers supplied, you need to use `get_publications`.

        Args:
            bibtex_fp: the filepath where the bibtex file is saved.

            args and kwargs are passed to `get_publications`.
        """
        verbose = get_verbose(kwargs)

        with open(bibtex_fp, "r") as f:
            bib_database = bibtexparser.load(f)

        # Retrieve the identifier from each bibtex entry
        identifiers = [
            self.librarian.bibtex_entry_identifier(entry)
            for entry in bib_database.entries
        ]
        identifiers = [id for id in identifiers if id is not None]
        if len(identifiers) < len(bib_database.entries) and verbose:
            warnings.warn(
                f"Only obtained {len(identifiers)} publications out of {len(bib_database.entries)} total due to missing identifiers."
            )

        # Query
        results = self.librarian.get_publications(identifiers, *args, **kwargs)
        # Validate
        publications = [
            result
            for result in results
            if (
                result is not None
                and result.publication_date is not None
                and result.abstract is not None
                # identifier will never be none
            )
        ]
        if len(publications) < len(identifiers) and verbose:
            warnings.warn(
                f"Only obtained {len(publications)} publications out of {len(identifiers)} total due to querying-related errors or missing abstracts."
            )

        # Construct atlas
        atl = Atlas(publications)
        return atl

    ######################################################################
    # Project Atlas
    ######################################################################

    def project(self, atl: Atlas, **kwargs) -> Atlas:
        """Update an atlas with its projection, i.e. the document embeddings for all publications using `self.vectorizer`, removing publications with no abstracts.

        Args:
            atl: the Atlas containing publications to project to document embeddings

            kwargs: keyword arguments propagated to `filter_by_func`

        Returns:
            the updated atlas containing all nonempty-abstract-containing publications and their projection
        """
        verbose = get_verbose(kwargs)

        # Only project publications that have abstracts and publication dates
        atl_filtered = self.filter_by_func(atl, **kwargs)
        num_empty = len(atl) - len(atl_filtered)
        if num_empty and verbose:
            warnings.warn(
                f"{num_empty} publications were filtered due to missing crucial data or incorrect field of study. There are now {len(atl_filtered.bad_ids)} total ids that will be excluded in the future."
            )

        # Project
        embeddings = None
        # get only embeddings for publications not already projected in atlas
        previously_embedded_ids = []
        if atl_filtered.projection is not None:
            previously_embedded_ids = atl_filtered.projection.identifier_to_index
        embed_ids = [
            id for id in atl_filtered.publications if id not in previously_embedded_ids
        ]

        fail_ids = set()
        if embed_ids:
            if verbose:
                if atl_filtered.projection is not None:
                    warnings.warn(
                        f"Found {len(atl_filtered.publications) - len(atl_filtered.projection)} publications not contained in Atlas projection."
                    )
                warnings.warn(f"Embedding {len(embed_ids)} total documents.")

            # Embed documents
            result = self.vectorizer.embed_documents(
                [atl_filtered[id].abstract for id in embed_ids],
                batch_size=kwargs["batch_size"] if "batch_size" in kwargs else None,
            )
            embeddings = result["embeddings"]
            success_indices = result["success_indices"]
            fail_indices = result["fail_indices"]

            # get new set of bad ids
            atl_filtered.bad_ids = atl_filtered.bad_ids.union(fail_ids)

            if fail_indices.tolist() and verbose:
                warnings.warn(
                    f"Failed to get embeddings for all {len(embed_ids)} publications; only {len(embeddings)} will be added to the Atlas. There are now {len(atl_filtered.bad_ids)} total ids that will be excluded in the future."
                )

            embed_ids_array = np.array(embed_ids)
            success_ids = embed_ids_array[success_indices]
            fail_ids = set(embed_ids_array[fail_indices])

            # create new projection
            projection = Projection(
                identifier_to_index={
                    identifier: idx for idx, identifier in enumerate(success_ids)
                },
                index_to_identifier=tuple(success_ids),
                embeddings=embeddings,
            )

        if not embed_ids or embed_ids is None and verbose:
            warnings.warn(f"Obtained no new publication embeddings.")
            projection = get_empty_projection()

        # merge existing projection with new projection
        merged_projection = merge(atl_filtered.projection, projection)

        # prepare to overwrite atlas with publications corresponding to updated (merged) projection
        embedded_publications = {
            id: pub
            for id, pub in atl_filtered.publications.items()
            if id in merged_projection.identifier_to_index
        }

        # Overwrite atlas data
        atl_filtered.publications = embedded_publications
        atl_filtered.projection = merged_projection
        return atl_filtered

    ######################################################################
    # Sort Atlas
    ######################################################################

    def sort(
        self,
        atl: Atlas,
        center: str,
    ) -> Tuple[list[str], list[str]]:
        """Sort an atlas according to cosine similarity to a center publication.
        Like numpy argsort, this returns identifiers that can be used to
        index the original atlas.

        Args:
            atl: the atlas to sort

            center: center the search on this publication

        Returns:
            sorted_keys: keys in descending order of similarity to the center publication
            sorted_values: values in descending order of similarity to the center publication
        """

        # If atlas is initial
        if atl.projection is None:
            atl = self.project(atl)
            if atl.projection is None:
                raise Exception(
                    f"Initial projection of atlas failed; make sure the initial publication has all the required attributes."
                )

        if len(atl.projection):
            # build cosine similarity matrix, of shape (1, num_pubs)
            cospsi_matrix = cosine_similarity(
                atl.projection.identifiers_to_embeddings([center]),
                atl.projection.embeddings,
            )
            # get most similar keys from center, including center itself
            sort_inds = np.argsort(cospsi_matrix)[-1][::-1]
            # argsort orders from least to greatest similarity, so reverse
            sorted_keys = atl.projection.indices_to_identifiers(sort_inds)
            sorted_values = cospsi_matrix[0][sort_inds]

            return sorted_keys, sorted_values

    ######################################################################
    # Expand Atlas
    ######################################################################

    def expand(
        self,
        atl: Atlas,
        *args,
        center: str = None,
        n_pubs_max: int = 4000,
        n_sources_max: int = None,
        record_pubs_per_update: bool = False,
        **kwargs,
    ) -> Atlas:
        """Expand an atlas by retrieving a list of publications resulting from traversal of the citation network.

        Args:
            atl: the atlas containing the region to expand

            center: (if given) center the search on this publication, preferentially searching related publications. Default is `None`, and the expansion is not centered. To keep a consistent expansion around one center, you should pass `atl.center`.

            n_pubs_max: maximum number of publications allowed in the expansion.

            n_sources_max: maximum number of publications (already in the atlas) to draw references and citations from.

            record_pubs_per_update: whether to track all the publications that exist in the resulting atlas to `self.pubs_per_update`. This should only be set to `True` when you need to later filter by degree of convergence of the atlas.

        Returns:
            atl_expanded: the expanded atlas
        """

        # Get the keys to expand
        expand_keys = None
        if center is not None:
            expand_keys = self.sort(atl, center)[0]

        # If that didn't work, just use all the keys
        existing_keys = set(atl.ids)
        if expand_keys is None:
            expand_keys = existing_keys

        if n_sources_max is not None:
            expand_keys = expand_keys[:n_sources_max]

        # Get identifiers for the expansion
        # For each publication corresponding to an id in `expand_keys`, collect the ids corresponding to the publication's references and citations.
        ids = set()
        for key in expand_keys:
            ids_i = set(atl[key].references + atl[key].citations)
            # Prune for obvious overlap, and for ids that have previously failed
            ids.update(ids_i - existing_keys - atl.bad_ids)
            # Break when the search is centered and we're maxed out
            if len(ids) > n_pubs_max and center is not None:
                break
        ids = list(ids)

        if not ids:
            print("Overly-restrictive search, no ids to retrive.")

        # Sample to account for max number of publications we want to retrieve
        if len(ids) > n_pubs_max:
            ids = np.random.choice(ids, n_pubs_max, replace=False)

        print(f"Expansion will include {len(ids)} new publications.")

        # Retrieve publications from ids using a librarian
        new_publications = self.librarian.get_publications(ids, *args, **kwargs)

        # New atlas
        atl_exp = Atlas(new_publications)

        # Update the new atlas
        atl_exp.publications.update(atl.publications)
        atl_exp.bad_ids = atl.bad_ids
        atl_exp.projection = (
            atl.projection
        )  # new projection will be updated in `project`
        atl_exp.center = atl.center

        # Record the new list of publications
        if record_pubs_per_update:
            self.pubs_per_update.append(list(atl_exp.ids))

        return atl_exp

    ######################################################################
    # Filter Atlas
    ######################################################################

    def filter_by_func(
        self,
        atl: Atlas,
        require_func: Callable[[Publication], bool] = lambda pub: pub_has_attributes(
            pub,
            attributes=[
                "abstract",
                "publication_date",
                "fields_of_study",
            ],
        ),
        record_pubs_per_update=False,
        **kwargs,
    ) -> Atlas:
        """Update an atlas by dropping publications (and corresponding data in projection) when certain fields are empty.

        Args:
            atl: the Atlas containing publications to filter

            require_func: a function that takes a publication and returns True if it should be kept in the atlas. For example, if `func = lambda pub: pub_has_attributes(pub, ["abstract"])`, then all publications that have `None` for the attribute `abstract` will be removed from the atlas, along with the corresponding data in the projection.

            record_pubs_per_update: whether to track all the publications that exist in the resulting atlas to `self.pubs_per_update`. This should only be set to `True` when you need to later filter by degree of convergence of the atlas. This is an important parameter because `self.filter` is called in `self.project`, which typically is called after `self.expand`, where we pass in the same parameter.

        Returns:
            the filtered atlas
        """
        # Filter publications
        invalid_pubs = {
            id: pub for id, pub in atl.publications.items() if not require_func(pub)
        }

        # Do not update if unnecessary
        if not len(invalid_pubs):
            return atl

        atl_filtered = self.filter_by_ids(atl, drop_ids=invalid_pubs.keys())

        # Record only the publications in the history that weren't filtered out
        if record_pubs_per_update:
            self.pubs_per_update[-1] = atl_filtered.ids

        return atl_filtered

    def filter_by_ids(
        self,
        atl: Atlas,
        keep_ids: list[str] = None,
        drop_ids: list[str] = None,
    ) -> Atlas:
        """Update an atlas by dropping publications (and corresponding data in projection).

        Args:
            atl: the Atlas containing publications to filter

            keep_ids: the list of publication ids to NOT filter; all other publications in `atl` not matching one of these ids will be removed.

            drop_ids: the list of publications to filter; all publications in `atl` matching one of these ids will be removed.
        """

        if all(x is not None for x in [keep_ids, drop_ids]):
            raise ValueError(
                "You must pass exactly one of `keep_ids` or `drop_ids`, but both had a value that was not `None`."
            )
        if keep_ids is not None:
            filter_ids = set([id for id in atl.ids if id not in keep_ids])
        elif drop_ids is not None:
            filter_ids = set(drop_ids)
        else:
            raise ValueError(
                "You must pass exactly one of `keep_ids` or `drop_ids`, but both had value `None`."
            )

        # Keep track of the bad identifiers to skip them in future expansions
        new_bad_ids = atl.bad_ids.union(filter_ids)

        # Filter embeddings, ids from projection
        if atl.projection is None:
            new_projection = None
        else:
            filter_indices = set()
            idx_to_id_new = []
            # From indexing
            for idx, id in enumerate(atl.projection.index_to_identifier):
                if id in filter_ids:
                    filter_indices.add(idx)
                else:
                    idx_to_id_new.append(id)
            # From embeddings
            embeddings = np.array(
                [
                    embedding
                    for idx, embedding in enumerate(atl.projection.embeddings)
                    if idx not in filter_indices
                ]
            )
            # From identifier to index map
            id_to_idx_new = {id: idx for idx, id in enumerate(idx_to_id_new)}
            # Construct new, filtered projection
            new_projection = Projection(
                identifier_to_index=id_to_idx_new,
                index_to_identifier=idx_to_id_new,
                embeddings=embeddings,
            )

        # Keep only filtered publications
        new_publications = [
            pub for id, pub in atl.publications.items() if id not in filter_ids
        ]

        # Construct new atlas
        atl_filtered = Atlas(new_publications, new_projection)
        atl_filtered.bad_ids = new_bad_ids

        # If the center was filtered out, then reset center
        atl_filtered.center = atl.center
        if atl_filtered.center not in atl_filtered.publications:
            atl_filtered.center = None

        return atl_filtered

    ########################################################################
    # Record Atlas history
    ########################################################################

    def track(
        self,
        atl: Atlas,
        calculate_convergence: bool = False,
        pubs: list[str] = None,
        pubs_per_update: list[list[str]] = None,
    ) -> Atlas:
        """Overwrite the data associated with tracking degree of convergence of publications in an atlas over multiple expansions. N.B.: the atlas must be fully projected, or else `converged_kernel_size` will raise a KeyError. By default, this function will overwrite the `atl.history` with updated `self.pubs_per_update`, but not `kernel_size`, which requires computing the converged kernel size for every publication in the atlas.

        Args:
            atl: the Atlas that will be updated by overwriting `Atlas.history`

            calculate_convergence: whether to call `self.converged_kernel_size`, and store the results in the `atl.history`.

            pubs: the list of publications to pass to `self.record_update_history`. By default `None`, and the most recent list of publications in the `self.update_history` list will be used.

            pubs_per_update: the list of lists of publications to pass to `self.record_update_history`. By default `None`, adn the full history in `self.update_history` will be used.

        Returns:
            atl the updated Atlas
        """
        print("Tracking atlas...")
        self.record_update_history(pubs, pubs_per_update)
        # Skip expensive convergence calculation if possible
        kernel_size = self.converged_kernel_size(atl) if calculate_convergence else None
        atl.history = {
            "pubs_per_update": self.pubs_per_update
            if pubs_per_update is None
            else pubs_per_update,
            "kernel_size": kernel_size,
        }
        return atl

    ########################################################################
    # Record Atlas history
    ########################################################################

    def record_update_history(
        self,
        pubs: list[str] = None,
        pubs_per_update: list[list[str]] = None,
    ) -> None:
        """Record when publications were added, by updating atl.update_history.

        atl.update_history is a np.array of ints representing when publications were added. A value of -2 indicates no record of being added.

        Args:
            pubs: a list of str ids corresponding to publications at the final update in the update history. By default `None`, and `self.pubs_per_update[-1]` will be used.

            pubs_per_update: a list of which publications existed at which iteration, with the index of the overall list corresponding to the iteration the publication was added. By default `None`, and `self.pubs_per_update` will be used.

        Updates:
            `self.update_history`: an np.array of ints representing when publications were added. A value of -2 indicates no record of being added.

        Returns:
            `None`
        """
        if pubs is None:
            pubs = self.pubs_per_update[-1]

        if pubs_per_update is None:
            pubs_per_update = self.pubs_per_update

        # Loop backwards
        i_max = len(pubs_per_update) - 1
        update_history = np.full(len(pubs), -2)
        for i, pubs_i in enumerate(pubs_per_update[::-1]):
            is_in = np.isin(pubs, pubs_i)
            update_history[is_in] = i_max - i
        self.update_history = update_history

    ########################################################################
    # Calculate Atlas convergence
    ########################################################################

    def converged_kernel_size(self, atl: Atlas) -> np.ndarray:
        """Calculate the largest size of the kernel that's converged (at differing levels of convergence) for each publication in a sample at each update.

        Args:
            atl: Atlas containing publications; for each publication we compute the largest converged kernel size at each update

        Returns:
            kernel_size: an array of ints of shape `(num_pubs, max_update)` representing the kernel size for converged kernels.
                - The first column indicates the largest kernel size that hasn't changed since the beginning,
                - The second column indicates the largest kernel size that hasn't changed since the first update,
                - etc. for the nth column.
        """
        print("Calculating degree of convergence for all publications.")
        if self.update_history is None:
            raise ValueError(
                "update_history is None; make sure you have called record_update_history()!"
            )

        if -2 in self.update_history:
            raise ValueError(
                "Incomplete update history as indicated by entries with values of -2."
            )

        publications = np.array(atl.ids)

        # Compute pairwise cosine similarity, shape `(num_pubs,num_pubs)`
        cospsi_matrix = batch_cospsi_matrix(atl.projection.embeddings)

        # 0. Loop over each publication
        cospsi_kernel: list[list[int]] = []
        for pub in tqdm(publications, desc="calculating converged kernel size"):
            # 1. Identify the similarity with the other publications relative to this publication, and sort accordingly.
            cospsi = cospsi_matrix[publications == pub].flatten()  # shape `(num_pubs,)`
            sort_inds = np.argsort(cospsi)[::-1]  # shape `(num_pubs,)`

            # 2. Identify the expansion iteration at which those publications were added to the atlas (`sorted_history`).
            sorted_history = self.update_history[sort_inds]  # shape `(num_pubs,)`

            # 3. Identify the latest iteration at which any publication was added to the atlas; this can be less than the total iterations.
            last_update = self.update_history.max()

            # 4. Loop through each iteration until `last_update`, and identify which publications were added at or before that iteration.
            result = [
                # 5. Compute how many publications out we can go and still only contain publications added at or before that iteration.
                # Use `argmin` to get the first instance of False
                # Finally, subtract 1: we want the first index before False.
                # See tests.test_cartography.TestConvergence.test_converged_kernel_size for a concrete example.
                np.argmin(sorted_history <= update_idx) - 1
                for update_idx in range(last_update)
            ]  # shape `(last_update, )`

            cospsi_kernel.append(result)

        return np.array(cospsi_kernel)

    ########################################################################
    # Measure Atlas topography
    ########################################################################

    def measure_topography(
        self,
        atl: Atlas,
        ids: list[str] = None,
        metrics: list[str] = ["density"],
        min_prior_pubs: int = 2,
        kernel_size=16,
        **kwargs,
    ):
        """Measure topographic properties of all publications relative to prior
        publications.

        Args:

            atl: the Atlas to measure

            publication_indices: an np.ndarray of ints representing the indices of publications in the Atlas projection to measure

            metrics: A list of strings representing the metrics to use. Options are...
                constant_asymmetry: The asymmetry of a publication $p_i$ w.r.t the entire atlas $\\{ p_j \\forall j \\in \\{1, ..., k\\} \\} where $k$ is the length of the atlas

                    $| \\sum_{j}^{k-1}( p_i - p_j ) |$

                kernel_constant_asymmetry: The asymmetry of a publication w.r.t. its kernel, { p_j for all j in {1, ..., k} } where k is `kernel_size`, i.e. the k nearest neighbors.

                density: the density of a publication's surrounding area, estimated by a heuristic inspired by mass / volume = k publications divided by the minimum arc length enclosing the furthest publication.

                    $\\frac{ k }{ smoothing\\_length(k) }$

                smoothing_length: The distance (in radians) to the farthest publication in the kernel, i.e. the kth nearest neighbor.

            min_prior_pubs: The minimum number of publications prior to the target publication for which to calculate the metric.

            kernel_size: the number of publications surrounding the publication for which to compute the topography metric, i.e. k nearest neighbors for k=kernel_size.

        Returns:
            estimates: an np.ndarray of shape `(len(publication_indices), len(metrics))` representing the estimated topography metric values for each publication.
        """
        _ = get_verbose(kwargs)

        # By default calculate for all publications
        if ids is None:
            ids = atl.ids
        else:
            ids = list(ids)

        if not ids:
            raise Exception("No publications to measure topography of.")

        # Get publication dates, for filtering
        dates = np.array([atl[identifier].publication_date for identifier in ids])

        # Get pairwise cosine similarities for ids
        embeddings = atl.projection.identifiers_to_embeddings(ids)
        cospsi_matrix = batch_cospsi_matrix(embeddings)

        # From here on, use embedding indices instead of identifiers
        # our embeddings are already in the correct order, so just use them
        publication_indices = np.arange(len(embeddings))

        print(f"Computing {metrics} for {len(ids)} publications.")
        estimates = []
        for idx, identifier in tqdm(enumerate(ids), total=len(ids)):
            # Get the date of publication
            date = atl[identifier].publication_date

            # Identify prior publications
            is_prior = dates < date
            if is_prior.sum() < min_prior_pubs:
                estimates.append([np.nan for _ in metrics])
                continue

            # Choose valid publications
            is_other = publication_indices != idx
            is_valid = is_prior & is_other
            valid_indices = publication_indices[is_valid]

            kwargs = {
                "idx": idx,
                "cospsi_matrix": cospsi_matrix,
                "valid_indices": valid_indices,
                "publication_indices": publication_indices,
                "embeddings": embeddings,
                "kernel_size": kernel_size,
            }

            def call_metric(
                metric: str,
                **kwargs,
            ) -> float:
                """Wrapper function to simplify topography metric api."""
                # Get the metric
                fn = getattr(topography, f"{metric}_metric")

                # Identify arguments to pass
                fn_args = inspect.getfullargspec(fn)
                used_kwargs = {}
                for key, value in kwargs.items():
                    if key in fn_args.args:
                        used_kwargs[key] = value
                # Call
                estimate = fn(**used_kwargs)
                return estimate

            estimates.append([call_metric(metric, **kwargs) for metric in metrics])

        estimates = np.array(estimates)

        return estimates
