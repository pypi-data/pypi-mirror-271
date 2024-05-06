from typing import List, Union

from .rates import ExchangeRate

def getRate(source: str, target: str, rates: List[ExchangeRate]) -> ExchangeRate:
    for rate in rates:
        if rate.source == source and rate.target == target:
            return rate
        
def getRateSumm(summ: Union[int, float], rate: ExchangeRate) -> Union[int, float]:
    return summ / rate.rate