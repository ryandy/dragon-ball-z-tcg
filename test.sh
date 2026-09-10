count=0
for seed in {1..10}; do
    dbz-play -d dbz/decks/goku_survival -d dbz/decks/goku_survival -ni --quiet -s ${seed}
    winner=$?
    if [ $winner -eq 0 ]; then
        ((count++))
    fi
done
echo $count
