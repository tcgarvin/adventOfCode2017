-- stack --install-ghc runghc

parseInput :: String -> [[Int]]
parseInput input = map parseLine (lines input)

parseLine :: String -> [Int]
-- I don't understand how this read x :: Int thing works yet.
parseLine line = map (\word -> read word :: Int) (words line)

checksum :: [[Int]] -> Int
checksum sheet = sum (map (\line -> maximum line - minimum line) sheet)

main = do 
    -- Still faking my way through IO. No idea how this works
    contents <- getContents
    print (checksum (parseInput contents))
