import hashlib
import time
import json

class MedicalRecord:
    def __init__(self, patient_id, doctor_id, diagnosis, prescription, timestamp=None):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'timestamp': self.timestamp
        }

class Block:
    def __init__(self, previous_hash, medical_record):
        self.timestamp = time.time()
        self.medical_record = medical_record
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = json.dumps({
            'timestamp': self.timestamp,
            'medical_record': self.medical_record.to_dict(),
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class HealthcareBlockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_record = MedicalRecord(
            "GENESIS",
            "SYSTEM",
            "Genesis Block",
            "No prescription",
        )
        genesis_block = Block("0", genesis_record)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_medical_record(self, patient_id, doctor_id, diagnosis, prescription):
        medical_record = MedicalRecord(patient_id, doctor_id, diagnosis, prescription)
        new_block = Block(self.get_latest_block().hash, medical_record)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_patient_records(self, patient_id):
        records = []
        for block in self.chain[1:]:  # Skip genesis block
            if block.medical_record.patient_id == patient_id:
                records.append(block.medical_record.to_dict())
        return records

# Example usage
def main():
    # Initialize blockchain
    healthcare_chain = HealthcareBlockchain()

    # Add some medical records
    healthcare_chain.add_medical_record(
        "P001",
        "DR_SMITH",
        "Common Cold",
        "Acetaminophen 500mg"
    )

    healthcare_chain.add_medical_record(
        "P001",
        "DR_JONES",
        "Follow-up visit",
        "Continue previous medication"
    )

    # Verify chain
    print("Blockchain valid:", healthcare_chain.is_chain_valid())

    # Get patient records
    records = healthcare_chain.get_patient_records("P001")
    print("\nPatient P001 Records:")
    for record in records:
        print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()