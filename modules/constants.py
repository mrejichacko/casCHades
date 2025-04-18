"""
Module defining constants related to file paths and column names.
"""

FOOD_WEB_MAPPING = {
    'EA_Alpines': 'data/foodwebs/EA_Alpines.csv',
    'cscf_EA_Alpines': 'data/foodwebs/cscf_EA_Alpines.csv',
    'EA_Lowlands': 'data/foodwebs/EA_Lowlands.csv',
    'cscf_EA_Lowlands': 'data/foodwebs/cscf_EA_Lowlands.csv',
    'JU_Alpines': 'data/foodwebs/JU_Alpines.csv',
    'cscf_JU_Alpines': 'data/foodwebs/cscf_JU_Alpines.csv',
    'JU_Lowlands': 'data/foodwebs/JU_Lowlands.csv',
    'cscf_JU_Lowlands': 'data/foodwebs/cscf_JU_Lowlands.csv',
    'MP_Alpines': 'data/foodwebs/MP_Alpines.csv',
    'cscf_MP_Alpines': 'data/foodwebs/cscf_MP_Alpines.csv',
    'MP_Lowlands': 'data/foodwebs/MP_Lowlands.csv',
    'cscf_MP_Lowlands': 'data/foodwebs/cscf_MP_Lowlands.csv',
    'NA_Alpines': 'data/foodwebs/NA_Alpines.csv',
    'cscf_NA_Alpines': 'data/foodwebs/cscf_NA_Alpines.csv',
    'NA_Lowlands': 'data/foodwebs/NA_Lowlands.csv',
    'cscf_NA_Lowlands': 'data/foodwebs/cscf_NA_Lowlands.csv',
    'SA_Alpines': 'data/foodwebs/SA_Alpines.csv',
    'cscf_SA_Alpines': 'data/foodwebs/cscf_SA_Alpines.csv',
    'SA_Lowlands': 'data/foodwebs/SA_Lowlands.csv',
    'cscf_SA_Lowlands': 'data/foodwebs/cscf_SA_Lowlands.csv',
    'WA_Alpines': 'data/foodwebs/WA_Alpines.csv',
    'cscf_WA_Alpines': 'data/foodwebs/cscf_WA_Alpines.csv',
    'WA_Lowlands': 'data/foodwebs/WA_Lowlands.csv',
    'cscf_WA_Lowlands': 'data/foodwebs/cscf_WA_Lowlands.csv'
}

ALL_SPECIES_AND_FOOD_GROUPS = 'data/node_lists/taxa_list.csv'


SOURCE_COL = "Source_Name"
TARGET_COL = "Target_Name"

#how often we print nodes
PRINT_SIZE = 1000

#Define the steps after which metrics are measured
METRIC_STEP_SIZE = 30
#METRIC_STEP_SIZE = 1

#Define the size of the bootstrap sample, starting with 0.05 or 5%
BOOTSTRAP_SIZE = 0.05

# EXEMPT_TERMS = set()
# Define the set of exempt terms representing the Feeding group
# EXEMPT_TERMS = {
#     "Acari", "Algae", "Annelida", "Moss", "Collembola", "Copepoda",
#     "Coprophagous", "Detritus", "Fungi", "Geophagous", "Keratophagous",
#     "Lichen", "Microbes", "Nematoda", "Osteophagous", "Plankton",
#     "Polyphagous - household", "POM", "Psocoptera", "Scavenger",
#     "Acartophthalmidae", "Agyrtidae", "Alexiidae", "Anisopodidae", "Asilidae",
#     "Asteiidae", "Atelestidae", "Aulacigastridae", "Bembix", "Blephariceridae",
#     "Bolitophilidae", "Byrrhidae", "Camillidae", "Campichoetidae",
#     "Canthyloscelidae", "Carnidae", "Ceratopogonidae", "Chamaemyiidae",
#     "Chaoboridae", "Chyromyidae", "Clambidae", "Clanoneurum", "Clusiidae",
#     "Coenomyiidae", "Corylophidae", "Crabro", "Cremifaniidae",
#     "Cryptophagidae", "Cucujidae", "Culicidae", "Cylindrotomidae",
#     "Diadocidiidae", "Diastatidae", "Ditomyiidae", "Dixidae", "Dryomyzidae",
#     "Dryopidae", "Elmidae", "Empididae", "Endomychidae", "Erotylidae",
#     "Eucinetidae", "Fanniidae", "Georissidae", "Heteroceridae",
#     "Hilarimorphidae", "Hybotidae", "Hydraenidae", "Hydrochidae",
#     "Hydrophilidae", "Kateretidae", "Keroplatidae", "Latridiidae", "Leiodidae",
#     "Lestica", "Lonchopteridae", "Megamerinidae", "Microphoridae",
#     "Mycetobiidae", "Olibrus", "Opetiidae", "Opomyzidae", "Pediciidae",
#     "Periscelididae", "Phalacrus", "Phoridae", "Psen", "Pseudopomyzidae",
#     "Psilidae", "Psliopora", "Psychodidae", "Ptiliidae", "Ptychopteridae",
#     "Pyrgotidae", "Rhagionidae", "Rhopalum", "Scatopsidae", "Scenopinidae",
#     "Scirtidae", "Sepsidae", "Silphidae", "Simuliidae", "Spercheidae",
#     "Sphaeroceridae", "Sphindidae", "Stenomicridae", "Stilbus",
#     "Stratiomyidae", "Strongylophthalmyiidae", "Tabanidae", "Tanypezidae",
#     "Thaumalaeidae", "Therevidae", "Tipulidae", "Trichoceridae",
#     "Trixoscelidae", "Ula", "Vermileonidae", "Xylomyidae", "Xylophagidae",
#     "Isopoda", "Exudativorous - honeydew", "Haematophagous", "Macrozoobenthos",
#     "Invertebrata", "Vertebrata", "Animalia", "Plantae"
# }

EXEMPT_TERMS = {
    "Acari", "Algae", "Annelida", "Moss", "Collembola", "Copepoda",
    "Coprophagous", "Detritus", "Fungi", "Geophagous", "Keratophagous",
    "Lichen", "Microbes", "Nematoda", "Osteophagous", "Plankton",
    "Polyphagous - household", "POM", "Psocoptera", "Scavenger",
    "Isopoda", "Exudativorous - honeydew", "Haematophagous", "Macrozoobenthos",
    "Invertebrata", "Vertebrata", "Animalia", "Plantae"
}