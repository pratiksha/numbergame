from ng import generators as gu

priors={gu.Root: 
        {gu.Or: 1./8,
         gu.And: 1./8,
         gu.Multiples: 1./8,
         gu.Interval: 1./8,
         gu.Contains: 1./8,
         gu.Primes: 1./8,
         gu.Powers: 1./8,
         gu.Equals: 1./8,}, 
        gu.Or: 
        {gu.Or: 0,
         gu.And: 0,
         gu.Multiples: 1./6,
         gu.Interval: 1./6,
         gu.Contains: 1./6,
         gu.Primes: 1./6,
         gu.Powers: 1./6,
         gu.Equals: 1./6,}, 
        gu.And: 
        {gu.Or: 0,
         gu.And: 0,
         gu.Multiples: 1./6,
         gu.Interval: 1./6,
         gu.Contains: 1./6,
         gu.Primes: 1./6,
         gu.Powers: 1./6,
         gu.Equals: 1./6,}, 
        } 
