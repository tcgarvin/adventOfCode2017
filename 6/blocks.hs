-- stack --install-ghc runghc

import Data.Word
import Data.Maybe
import Data.Ix
import Data.Bool
import qualified Data.Set as Set
import qualified Data.ByteString as B

import Debug.Trace

-- A bit of a hack.  The number of blocks per bank looks like it will stay
-- well under 256 in all cases so we can pack it all into a ByteString
-- instead of learning how to make my own Ord for the set.
parseInput :: String -> B.ByteString
parseInput input = B.pack (map(\word -> read word :: Word8) (words input))

cyclesUntilRepeat :: B.ByteString -> Int
cyclesUntilRepeat banks = recurse banks Set.empty

-- As in puzzle 5, concerned about modification
recurse :: B.ByteString -> Set.Set B.ByteString -> Int
recurse banks seen -- | trace (show (B.unpack banks)) False = undefined
                   | Set.member banks seen = 0
                   | otherwise = (recurse (balance banks) (Set.insert banks seen)) + 1


-- I keep writing this helper, so I must be missing something.
enumerate :: B.ByteString -> [(Int, Word8)]
enumerate l = zip (range (0, (B.length l))) (B.unpack l)


-- There are at least two searches here. On the plus side, balancef is being
-- partially applied before being used by the map, so that's cool.
balance :: B.ByteString -> B.ByteString
balance banks = B.pack (map partial (enumerate banks))
    where maxBlocks = B.maximum banks
          partial = balancef (fromIntegral maxBlocks :: Int) (fromJust (B.elemIndex maxBlocks banks)) (B.length banks)

balancef :: Int -> Int -> Int -> (Int, Word8) -> Word8
-- balancef numBlocks maxIndex length elem | trace ("" ++ show numBlocks ++ ", " ++ show maxIndex ++ ", " ++ show length ++ ", " ++ show elem) False = undefined
balancef numBlocks maxIndex length elem = (baseValue maxIndex elem) + (fromIntegral (quot numBlocks length) :: Word8) + (oneOrNone maxIndex (fst elem) (rem numBlocks length) length)

baseValue :: Int -> (Int, Word8) -> Word8
baseValue maxIndex elem | (fst elem) == maxIndex = 0
                        | otherwise = snd elem

oneOrNone :: Int -> Int -> Int -> Int -> Word8
-- oneOrNone i j diff length | trace(show i ++ ", " ++ show j ++ ", " ++ show diff ++ ", " ++ show length) False = undefined
oneOrNone i j diff length = bool 0 1 ((mod (j - i - 1) length) < diff)

main = do
    input <- getContents
    let banks = parseInput input
    print (cyclesUntilRepeat banks)
