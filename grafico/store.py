

from grafico.atoms import ConceptualAtoms


class MoleculeStore():
    _molecules: dict[str, ConceptualAtoms]  # maps iri to ConceptualAtoms

    def __init__(self):
        self._molecules = {}

    def save(self, atoms: ConceptualAtoms) -> None:
        self._molecules[atoms.iri] = atoms

    def get(self, iri: str) -> ConceptualAtoms | None:
        return self._molecules.get(iri)
