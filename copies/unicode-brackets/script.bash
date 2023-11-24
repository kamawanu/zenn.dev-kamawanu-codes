while IFS=';' read number name category rest
do 
    if [[ "$category" =~ Ps|Pe|Pi|Pf ]]
    then 
        printf "%s (U+%s, %s): \u"$number"\n" "$name" "$number" "$category"
    fi
done <UnicodeData.txt
