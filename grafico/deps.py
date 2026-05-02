
from dataclasses import dataclass

from grafico.store import MoleculeStore

@dataclass
class GraficoDeps:
    store: MoleculeStore

# the high-level idea:
# the LLM will need to call the lookup_molecule tool.
# that tool needs a MoleculeStore argument.
# LLMs can generate strings and numbers, but not a MoleculeStore.
# so, we need a MoleculeStore dependency.