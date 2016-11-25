from ng import generators as gu

priors= {gu.Root: 
         {gu.Or: 1./8,
         gu.And: 1./8,
         gu.Multiples: 0.45,
         gu.Interval: 0.05,
         gu.Contains: 1./16,
         gu.Primes: 1./16,
         gu.Powers: 1./16,
         gu.Equals: 1./16,},
        gu.And:
        {gu.Or: 0,
         gu.And: 0,
         gu.Multiples: 1./3,
         gu.Interval: 0,
         gu.Contains: 1./6,
         gu.Primes: 1./6,
         gu.Powers: 1./6,
         gu.Equals: 1./6,},
        gu.Or:
        {gu.Or: 0,
         gu.And: 0,
         gu.Multiples: 1./30,
         gu.Interval: 0.3,
         gu.Contains: 1./6,
         gu.Primes: 1./6,
         gu.Powers: 1./6,
         gu.Equals: 1./6,},
        }
