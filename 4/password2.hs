-- stack --install-ghc runghc

-- This one give me an import error?
-- import qualified Data.HashSet as HashSet
import qualified Data.Set as Set
import Data.List

-- In not-haskell, I would just fail as soon as I see a duplicate word, but
-- this works for now.
setOfReorderedTokens :: [[Char]] -> Set.Set [Char]
setOfReorderedTokens tokens = Set.fromList (map (\token -> sort token) tokens)

validate :: String -> Bool
validate phrase = Set.size (setOfReorderedTokens tokens) == length tokens
    where tokens = words phrase

filterBadPassphrases :: [String] -> [String]
filterBadPassphrases phrases = filter validate phrases

main = do
    contents <- getContents
    let passphrases = lines contents
    print (length (filterBadPassphrases passphrases))
