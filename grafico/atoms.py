from pydantic import BaseModel, field_validator
import selfies as sf


class ConceptualAtoms(BaseModel):  
    iri: str
    name: str
    selfies: str
    molecular_formula: str
    molecular_weight: float

    @field_validator('selfies')
    @classmethod
    def check_selfies(class_, selfies_value):
        if (not sf.decoder(selfies_value)):
            raise ValueError("Invalid SELFIES string")
        
        return selfies_value



# atom = ConceptualAtoms(iri="huh", name="ethanol", selfies=sf.encoder("CCO"), molecular_formula="C2H50H", molecular_weight=40)
# print(atom)
