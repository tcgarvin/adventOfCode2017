-- stack --install-ghc runghc

import System.Environment

coordinates :: Int -> (Int, Int) -- X,Y

coordinates 1 = (0,0)
coordinates 2 = (1,0)
coordinates t | px > 0 && px > abs py     = (px  , py+1)
              | py > 0 && py > negate px  = (px-1, py  )
              | px < 0 && px < py         = (px  , py-1)
              | py < 0 && py <= negate px = (px+1,py  )
    where pc = coordinates(t-1) 
          px = fst pc
          py = snd pc

manhattanDistance :: (Int, Int) -> Int
manhattanDistance coords = abs (fst coords) + abs (snd coords)


main = do 
    args <- getArgs  --Still no idea
    let target = read (head args) :: Int  --Still no idea
    print (manhattanDistance (coordinates target))
