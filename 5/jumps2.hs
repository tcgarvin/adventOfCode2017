-- stack --install-ghc runghc

-- This version tries to make it a more clear-cut tail-recursion.
-- It's still real slow.  Real, real slow.

import Data.Ix
import Data.Array

parseInput :: [String] -> [Int]
parseInput numbers = map(\number -> read number :: Int) numbers

-- Small pieces
inc :: Int -> Int
inc x = x + 1

-- Turn [x,y,z] into [(0,x),(1,y),(2,z)]
enumerate :: [a] -> [(Int, a)]
enumerate l = zip (range (0, (length l))) l

-- Turn a list into an array. Couldn't find it in Hoogle
toArray :: [a] -> Array Int a
toArray numbers = array (0, ((length numbers) - 1)) (enumerate numbers)

-- Simpler entry function for recursion
countJumpsToEscape :: [Int] -> Int
countJumpsToEscape jumps = recurse (toArray jumps) 0 0

-- Jump recusively.  This seems harder to read than if it had been imperitive
-- On the fun side, this had to recurse about 370000 times
recurse :: Array Int Int -> Int -> Int -> Int
recurse jumps i depth | (i < 0 || i >= length jumps) = depth
                      | otherwise = recurse (incrementJump jumps i) (jumps ! i + i) (depth + 1)

-- Increment one point in the jump array by one.  Haskell seems to claim that
-- this is going to be reasonably efficient even though it's immutable, but I
-- don't know how to think of this as other than a full copy.
incrementJump :: Array Int Int -> Int -> Array Int Int
incrementJump jumps i = jumps // [(i, oneOrThree (jumps ! i))]

oneOrThree :: Int -> Int
oneOrThree offset | offset >= 3 = offset - 1
                  | otherwise = inc offset


main = do
    input <- getContents
    let jumps = parseInput (lines input)
    print (countJumpsToEscape jumps)
