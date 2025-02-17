import json
import logging
from datetime import datetime
from Bio.PDB import PDBParser, Select, PDBIO

logger = logging.getLogger(__name__)


def load_map_file(map_file):
    with open(map_file, 'r') as f:
        mapping = json.load(f)
    return mapping

def parse_pdb_and_validate(pdb_file):
    is_valid = False

    # Create a PDBParser object
    parser = PDBParser()

    # Parse the PDB file
    try:
        structure = parser.get_structure('ProteinDataBank', pdb_file)
    except Exception as e:
        logger.error(f"Error in parsing PDB file: {e}")
        return is_valid

    # Print the structure
    atoms = []
    required_atoms = {'CA', 'C', 'N', 'O'}
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    atoms.append(atom.name)

    missing_atoms = required_atoms - set(atoms)
    if missing_atoms:
        logger.error(f"Missing atoms: {missing_atoms}")
        logger.error("PDB file is invalid")
    else:
        logger.info("All required atoms are present")
        logger.info("PDB file is valid")
        is_valid = True

    return is_valid

class ChainSelect(Select):
    def __init__(self, chain_ids):
        self.chain_ids = chain_ids

    def accept_chain(self, chain):
        return chain.id in self.chain_ids

def extract_chains(pdb_file, output_file, chain_ids) -> dict:
    load_map = load_map_file('mapping.json')

    # Create a PDBParser object
    parser = PDBParser()

    # Parse the PDB file
    structure = parser.get_structure('ProteinDataBank', pdb_file)

    # Create a PDBIO object
    io = PDBIO()

    # Set the structure to be saved
    io.set_structure(structure)

    # Save only the selected chains
    io.save(output_file, ChainSelect(chain_ids))

    # # Get the protein ID and current date and time
    protein_id = structure.id
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate the length of each chain
    chains = {chain.id: chain for chain in structure.get_chains() if chain.id in chain_ids}
    chain_res_names = {chain_id: [residue.resname for residue in chain] for chain_id, chain in chains.items()}
    chain_sequences = {chain_id: "" for chain_id in chain_ids}

    # Write additional information to the output file
    with open(output_file, 'a') as f:
        f.write(f"\nREMARK Protein ID: {protein_id}\n")
        f.write(f"REMARK Date and Time of Processing: {current_time}\n")
        for chain_id, length in chains.items():
            sequence = [load_map[val] for val in chain_res_names[chain_id] if val in load_map]
            chain_sequences[chain_id] = "".join(sequence)
            f.write(f"REMARK Chain {chain_id} Sequence: {chain_sequences[chain_id]}\n")
            f.write(f"REMARK Chain {chain_id} Length: {len(sequence)}\n")

    return chain_sequences

