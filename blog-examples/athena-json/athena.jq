[{UserPages: {S: "PK"}}, {SortKey: {S: "SK"}}] + [.ResultSet.Rows[1:4][] | {(.Data[0].VarCharValue): {N: .Data[1].VarCharValue}}] | add | tostring
