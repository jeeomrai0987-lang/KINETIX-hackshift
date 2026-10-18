from sqlalchemy.orm import Session
from database.models.worker_profile import WorkerProfile
from database.seed.cast import (
    USR_WORKER_03,
    USR_WORKER_04,
    USR_WORKER_05
)
from database.seed.seed_worker_people import (
    USR_WORKER_EXTRA_1,
    USR_WORKER_EXTRA_2,
    USR_WORKER_EXTRA_3
)

PHASE = 20


def seed(db: Session):
    profiles = [
        # 1. Elena Vance (usr_worker_03)
        WorkerProfile(
            user_id=USR_WORKER_03,
            experience_level="senior",
            skills=[
                "Distributed Systems",
                "Rust",
                "Go",
                "System Architecture",
                "Fintech Protocols"
            ],
            portfolio_url="https://elenavance.dev",
            github_url="https://github.com/elena-vance-dist",
            phone="+1 (555) 382-9014",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=20,
            percentile=96.4
        ),
        # 2. Julian Vance (usr_worker_04)
        WorkerProfile(
            user_id=USR_WORKER_04,
            experience_level="founding",
            skills=[
                "Distributed Systems",
                "Rust",
                "Raft Consensus",
                "Kubernetes Operator",
                "MicroVM"
            ],
            portfolio_url="https://julianvance.tech",
            github_url="https://github.com/julian-vance",
            phone="+1 (555) 345-6789",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=30,
            percentile=98.2
        ),
        # 3. Elena Rostova (usr_worker_05)
        WorkerProfile(
            user_id=USR_WORKER_05,
            experience_level="senior",
            skills=[
                "Wasm Runtime",
                "Sandbox Isolation",
                "eBPF",
                "C/C++",
                "Audit Attestation"
            ],
            portfolio_url="https://rostova.security",
            github_url="https://github.com/elena-rostova",
            phone="+1 (555) 456-7890",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=20,
            percentile=94.8
        ),
        # 4. Alex Chen (usr_worker_extra_1)
        WorkerProfile(
            user_id=USR_WORKER_EXTRA_1,
            experience_level="senior",
            skills=[
                "Wasmtime",
                "eBPF",
                "Rust",
                "MicroVM Sandboxing",
                "Kernel Tracing"
            ],
            portfolio_url="https://alexchen.dev",
            github_url="https://github.com/alexchen-wasm",
            phone="+1 (555) 567-8901",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=20,
            percentile=92.5
        ),
        # 5. Rachel Zhang (usr_worker_extra_2)
        WorkerProfile(
            user_id=USR_WORKER_EXTRA_2,
            experience_level="senior",
            skills=[
                "Rust Core",
                "Memory Layouts",
                "Zero-Copy IO",
                "LSM-Trees",
                "C++"
            ],
            portfolio_url="https://rachelzhang.io",
            github_url="https://github.com/rachelz-storage",
            phone="+1 (555) 678-9012",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=25,
            percentile=93.1
        ),
        # 6. David Kim (usr_worker_extra_3)
        WorkerProfile(
            user_id=USR_WORKER_EXTRA_3,
            experience_level="mid",
            skills=[
                "Go",
                "Distributed State",
                "gRPC",
                "Zero-Copy IO",
                "Fintech Protocols"
            ],
            portfolio_url="https://davidkim.codes",
            github_url="https://github.com/davidkim-dist",
            phone="+1 (555) 789-0123",
            whatsapp_enabled=True,
            cloaked=True,
            weekly_availability_hours=20,
            percentile=90.4
        ),
    ]

    db.add_all(profiles)
    db.flush()


def run(db: Session):
    seed(db)

