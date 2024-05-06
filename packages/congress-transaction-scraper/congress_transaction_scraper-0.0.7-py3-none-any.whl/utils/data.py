from dataclasses import dataclass, field
from typing import List, Dict

STATES = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


@dataclass
class ScrapedTransaction:
    date: str
    owner: str
    ticker: str
    asset_name: str
    asset_type: str
    transaction_type: str
    amount: str
    comment: str

    @classmethod
    def from_dict(cls, record: Dict):
        return cls(
            date=record["Transaction Date"],
            owner=record["Owner"],
            ticker=record["Ticker"],
            asset_name=record["Asset Name"],
            asset_type=record["Asset Type"],
            transaction_type=record["Type"],
            amount=record["Amount"],
            comment=record["Comment"],
        )

    def __str__(self):
        return f"{self.asset_name} {self.transaction_type} on {self.date}"


@dataclass
class ScrapedDisclosure:
    url: str
    office: str
    first_name: str
    last_name: str
    state: str
    disclosure_type: str
    date: str
    html: str
    image: bool = False
    transactions: List[ScrapedTransaction] = field(default_factory=list)

    def __str__(self):
        return f"{self.disclosure_type} for {self.first_name} {self.last_name}"
