for i in functions/*.py; do
    [ -f "$i" ] || break
    echo "$i"
done