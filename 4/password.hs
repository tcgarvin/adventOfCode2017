-- stack --install-ghc runghc

-- This one give me an import error?
-- import qualified Data.HashSet as HashSet
import qualified Data.Set as Set

-- In not-haskell, I would just fail as soon as I see a duplicate word, but
-- this works for now.
validate :: String -> Bool
validate phrase = Set.size (Set.fromList (words phrase)) == length (words phrase)

filterBadPassphrases :: [String] -> [String]
filterBadPassphrases phrases = filter validate phrases

main = do
    contents <- getContents
    let passphrases = lines contents
    print (length (filterBadPassphrases passphrases))
