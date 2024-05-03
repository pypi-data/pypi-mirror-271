# py-coldp
 Python tools for working with taxonomic checklists organised as Catalogue of Life Data Package (COLDP) format

# Overview
py-coldp is a Python package to facilitate creation, manipulation, editing and serialisation of taxonomic checklists in the [Catalogue of Life Data Package](https://github.com/CatalogueOfLife/coldp ) format.

The package includes two classes:
* **[COLDP](#class-coldp)** - A COLDP package loaded as a set of Pandas dataframes
* **[NameBundle](#class-namebundle)** - A helper class to simplify addition of taxon names with sets of associated synonyms to a COLDP instance

# Class: COLDP
The main class instantiates a COLDP package in memory as a set of Pandas dataframes. An instance may be initialised from the contents of a folder containing a set of COLDP-compliant CSV or tab-delimited data files or alternatively can be initialised as an empty instance in memory. The class includes many methods for inserting new data, editing existing records and querying the contents of the package. The instance can then be saved as a set of CSV files in a named folder .

__init__(self, folder, name, **kwargs)

set(self, **kwargs)
set_options(self, options)

set_context(self, context)

initialise_dataframe(self, foldername, name, default_headings)
extract_table(self, df, headings, mappings)
fix_basionyms(self, names, synonyms)
fix_classification(self)
fix_classification_recursive(self, taxa, ranks, parent)
sort_taxa(self)
sort_taxa_recursive(self, df, ids, id)
sort_names(self)
table_by_name(self, name)
reset_ids(self, name=None, prefix=None)
add_references(self, reference_list)
get_reference(self, id)
find_reference(self, reference)
start_name_bundle(self, accepted, incertae_sedis=False, sic=False)
add_names(self, bundle, parent)
add_name_relation(self, name_relation)
add_type_material(self, type_material)
add_distribution(self, distribution)
add_species_interaction(self, interaction)
prepare_bundle(self, bundle)
add_synonym(self, taxon_id, name_id)
add_taxon(self, name, parent, incertae_sedis=False)
modify_taxon(self, taxon_id, properties)
modify_name(self, name_id, properties)
identify_name(self, name)
same_basionym(self, a, b)
remove_gender(self, epithet)
get_original_authorship(self, authorship)
epithet_and_authorship_match(self, name, epithet, authorship)
set_basionymid(self, name, basionymid)
fix_basionymid(self, name, synonyms)
find_name_record(self, name)
get_name(self, id)
find_name(self, scientificName, authorship, rank)
find_taxon(self, scientificName, authorship, rank)
find_names(self, properties, to_dict=False)
get_taxon(self, id)
get_synonyms(self, taxonID, to_dict=False)
get_synonymy(self, nameID, to_dict=False)
get_children(self, taxonID, to_dict=False)
get_text_tree(self, taxonID, indent="")
construct_species_rank_name(self, g, sg, s, ss, marker)
construct_authorship(self, a, y, is_basionym)
is_species_group(self, name)
is_infrasubspecific(self, name)
save(self, destination=None, name=None)
issue(self, message, **record)


# Class: NameBundle

__init__(self, coldp, accepted: dict, incertae_sedis: bool = False, sic: bool = False) -> None
add_synonym(self, synonym dict, sic bool = False) -> None
normalise_name(self, name dict, sic bool = False) -> dict
derive_name(self, name dict, values dict, sic bool = False) -> dict