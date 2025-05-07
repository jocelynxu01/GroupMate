import torch

arxiv_cs_categories = [
    "cs.AI",  # Artificial Intelligence
    "cs.AR",  # Hardware Architecture
    "cs.CC",  # Computational Complexity
    "cs.CE",  # Computational Engineering, Finance, and Science
    "cs.CG",  # Computational Geometry
    "cs.CL",  # Computation and Language
    "cs.CR",  # Cryptography and Security
    "cs.CV",  # Computer Vision and Pattern Recognition
    "cs.CY",  # Computers and Society
    "cs.DB",  # Databases
    "cs.DC",  # Distributed, Parallel, and Cluster Computing
    "cs.DL",  # Digital Libraries
    "cs.DM",  # Discrete Mathematics
    "cs.DS",  # Data Structures and Algorithms
    "cs.ET",  # Emerging Technologies
    "cs.FL",  # Formal Languages and Automata Theory
    "cs.GL",  # General Literature
    "cs.GR",  # Graphics
    "cs.GT",  # Computer Science and Game Theory
    "cs.HC",  # Human-Computer Interaction
    "cs.IR",  # Information Retrieval
    "cs.IT",  # Information Theory
    "cs.LG",  # Machine Learning
    "cs.LO",  # Logic in Computer Science
    "cs.MA",  # Multiagent Systems
    "cs.MM",  # Multimedia
    "cs.MS",  # Mathematical Software
    "cs.NA",  # Numerical Analysis
    "cs.NE",  # Neural and Evolutionary Computing
    "cs.NI",  # Networking and Internet Architecture
    "cs.OH",  # Other Computer Science
    "cs.OS",  # Operating Systems
    "cs.PF",  # Performance
    "cs.PL",  # Programming Languages
    "cs.RO",  # Robotics
    "cs.SC",  # Symbolic Computation
    "cs.SD",  # Sound
    "cs.SE",  # Software Engineering
    "cs.SI",  # Social and Information Networks
    "cs.SY",  # Systems and Control
]


arxiv_all_categories = [
    # Computer Science
    "cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR", "cs.CV", "cs.CY",
    "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS", "cs.ET", "cs.FL", "cs.GL", "cs.GR",
    "cs.GT", "cs.HC", "cs.IR", "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS",
    "cs.NA", "cs.NE", "cs.NI", "cs.OH", "cs.OS", "cs.PF", "cs.PL", "cs.RO", "cs.SC",
    "cs.SD", "cs.SE", "cs.SI", "cs.SY",

    # Mathematics
    "math.AC", "math.AG", "math.AP", "math.AT", "math.CA", "math.CO", "math.CT", "math.CV",
    "math.DG", "math.DS", "math.FA", "math.GM", "math.GN", "math.GR", "math.GT", "math.HO",
    "math.IT", "math.KT", "math.LO", "math.MG", "math.MP", "math.NA", "math.NT", "math.OA",
    "math.OC", "math.PR", "math.QA", "math.RA", "math.RT", "math.SG", "math.SP", "math.ST",

    # Physics
    "astro-ph", "cond-mat", "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th", "math-ph",
    "nlin", "nucl-ex", "nucl-th", "physics", "quant-ph",

    # Quantitative Biology
    "q-bio.BM", "q-bio.CB", "q-bio.GN", "q-bio.MN", "q-bio.NC", "q-bio.OT", "q-bio.PE", "q-bio.QM",
    "q-bio.SC", "q-bio.TO",

    # Quantitative Finance
    "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM", "q-fin.PR", "q-fin.RM", "q-fin.ST",
    "q-fin.TR",

    # Statistics
    "stat.AP", "stat.CO", "stat.ME", "stat.ML", "stat.OT", "stat.TH",

    # Electrical Engineering and Systems Science (EESS)
    "eess.AS", "eess.IV", "eess.SP", "eess.SY",

    # Economics
    "econ.EM", "econ.GN", "econ.TH"
]



CATEGORY_MAP = {
    # Computer Science
    "cs.AI": "artificial intelligence",
    "cs.AR": "hardware architecture",
    "cs.CC": "computational complexity",
    "cs.CE": "computer engineering",
    "cs.CG": "computational geometry",
    "cs.CL": "natural language processing",
    "cs.CR": "cryptography and security",
    "cs.CV": "computer vision",
    "cs.CY": "computers and society",
    "cs.DB": "databases",
    "cs.DC": "distributed computing",
    "cs.DL": "digital libraries",
    "cs.DM": "discrete mathematics",
    "cs.DS": "data structures and algorithms",
    "cs.ET": "emerging technologies",
    "cs.FL": "formal languages and automata",
    "cs.GL": "general computer science",
    "cs.GR": "graph theory",
    "cs.GT": "game theory",
    "cs.HC": "human-computer interaction",
    "cs.IR": "information retrieval",
    "cs.IT": "information theory",
    "cs.LG": "machine learning",
    "cs.LO": "logic in computer science",
    "cs.MA": "multiagent systems",
    "cs.MM": "multimedia",
    "cs.MS": "mathematical software",
    "cs.NA": "numerical analysis",
    "cs.NE": "neural networks",
    "cs.NI": "networking and internet architecture",
    "cs.OH": "other computer science",
    "cs.OS": "operating systems",
    "cs.PF": "performance",
    "cs.PL": "programming languages",
    "cs.RO": "robotics",
    "cs.SC": "symbolic computation",
    "cs.SD": "sound",
    "cs.SE": "software engineering",
    "cs.SI": "social and information networks",
    "cs.SY": "systems and control",

    # Mathematics
    "math.AC": "commutative algebra",
    "math.AG": "algebraic geometry",
    "math.AP": "analysis of PDEs",
    "math.AT": "algebraic topology",
    "math.CA": "classical analysis",
    "math.CO": "combinatorics",
    "math.CT": "category theory",
    "math.CV": "complex variables",
    "math.DG": "differential geometry",
    "math.DS": "dynamical systems",
    "math.FA": "functional analysis",
    "math.GM": "general mathematics",
    "math.GN": "general topology",
    "math.GR": "group theory",
    "math.GT": "geometric topology",
    "math.HO": "history of mathematics",
    "math.IT": "information theory",
    "math.KT": "K-theory and homology",
    "math.LO": "logic",
    "math.MG": "metric geometry",
    "math.MP": "mathematical physics",
    "math.NA": "numerical analysis",
    "math.NT": "number theory",
    "math.OA": "operator algebras",
    "math.OC": "optimization and control",
    "math.PR": "probability",
    "math.QA": "quantum algebra",
    "math.RA": "rings and algebras",
    "math.RT": "representation theory",
    "math.SG": "symplectic geometry",
    "math.SP": "stochastic processes",
    "math.ST": "statistics",

    # Physics
    "astro-ph": "astrophysics",
    "cond-mat": "condensed matter physics",
    "gr-qc": "general relativity and quantum cosmology",
    "hep-ex": "high energy physics - experiment",
    "hep-lat": "high energy physics - lattice",
    "hep-ph": "high energy physics - phenomenology",
    "hep-th": "high energy physics - theory",
    "math-ph": "mathematical physics",
    "nlin": "nonlinear sciences",
    "nucl-ex": "nuclear experiment",
    "nucl-th": "nuclear theory",
    "physics": "general physics",
    "quant-ph": "quantum physics",

    # Quantitative Biology
    "q-bio.BM": "biomolecules",
    "q-bio.CB": "cell behavior",
    "q-bio.GN": "genomics",
    "q-bio.MN": "molecular networks",
    "q-bio.NC": "neuroscience",
    "q-bio.OT": "other quantitative biology",
    "q-bio.PE": "populations and evolution",
    "q-bio.QM": "quantitative methods",
    "q-bio.SC": "subcellular processes",
    "q-bio.TO": "tissues and organs",

    # Quantitative Finance
    "q-fin.CP": "computational finance",
    "q-fin.EC": "economics",
    "q-fin.GN": "general quantitative finance",
    "q-fin.MF": "mathematical finance",
    "q-fin.PM": "portfolio management",
    "q-fin.PR": "pricing of securities",
    "q-fin.RM": "risk management",
    "q-fin.ST": "statistical finance",
    "q-fin.TR": "trading and market microstructure",

    # Statistics
    "stat.AP": "applied statistics",
    "stat.CO": "computational statistics",
    "stat.ME": "methodology",
    "stat.ML": "statistical machine learning",
    "stat.OT": "other statistics",
    "stat.TH": "theory",

    # Electrical Engineering and Systems Science (EESS)
    "eess.AS": "audio and speech processing",
    "eess.IV": "image and video processing",
    "eess.SP": "signal processing",
    "eess.SY": "systems and control",

    # Economics
    "econ.EM": "econometrics",
    "econ.GN": "general economics",
    "econ.TH": "economic theory"
}



# model training configs
MODEL_NAME = "allenai/scibert_scivocab_uncased"
BATCH_SIZE = 16
EPOCHS = 20
LR = 2e-5
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
PATIENCE = 3


