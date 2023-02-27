.ResultSet.Rows[1:] |
{
    PageTrackTable: [
        group_by(.Data[0].VarCharValue)[] |
        {
            PutRequest:
            {
                Item:
                ({
                    UserPages: {S: "Richard"},
                    SortKey:   {S: ("PAGES#" + .[0].Data[0].VarCharValue)},
                } + ([.[] | {(.Data[1].VarCharValue): {"N": .Data[2].VarCharValue }}] | add))
            }
        }
    ]
}
| tostring
