# Turn a DynamoDb result with days as attributes into a daily frequency array
.Items[] | {
    File: .UserPages.S,
    Month: .SortKey.S[7:],
    Days: (to_entries |
        map(select(.key | startswith("D")) |  # Filter items that are days
        {
            # Format as {day: count}
            key: (.key[1:] | tonumber),
            value: (.value.N | tonumber)
        }) |
        reduce .[] as $i ([]; .[$i.key] = $i.value) | [.[] | . // 0] # turn into null-padded array
    )
}
