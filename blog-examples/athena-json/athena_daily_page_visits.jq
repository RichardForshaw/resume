.ResultSet.Rows[1:] | group_by(.Data[0].VarCharValue)[] |
{
    PageTrackTable: [
        group_by(.Data[1].VarCharValue)[] |
        {
            PutRequest:
            {
                Item:
                ({
                    UserPages: {S: ("Richard#"+.[0].Data[0].VarCharValue)},
                    SortKey:   {S: ("VISITS#" + .[0].Data[1].VarCharValue)},
                } + ([.[] | {("D"+.Data[2].VarCharValue): {"N": .Data[3].VarCharValue }}] | add))
            }
        }
    ]
}
| tostring
