import logging

from utils.extract import extract_chains, parse_pdb_and_validate
from utils.model_request import generate_results

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("prediction-app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    validate_file = parse_pdb_and_validate('input/1bey.pdb')
    if validate_file:
        sequences = extract_chains('input/1bey.pdb', 'output/extracted.pdb', ['H', 'L'])
        generate_results(sequences)


