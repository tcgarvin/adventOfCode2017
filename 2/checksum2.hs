-- stack --install-ghc runghc

import Data.List
import Data.Maybe

parseInput :: String -> [[Int]]
parseInput input = map parseLine (lines input)

parseLine :: String -> [Int]
-- I don't understand how this read x :: Int thing works yet.
parseLine line = map (\word -> read word :: Int) (words line)

checksum :: [[Int]] -> Int
checksum sheet = sum (map (\line -> (uncurry quot) (findOperands line)) sheet)

findOperands :: [Int] -> (Int, Int)
findOperands row = fromJust (find (\(a,b) -> (a /= b) && ((rem a b) == 0)) [(a,b) | a <- row, b <- row])

main = do 
    -- Still faking my way through IO. No idea how this works
    contents <- getContents
    print (checksum (parseInput contents))
