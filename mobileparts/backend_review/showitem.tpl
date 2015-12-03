<h1>Things to bring to our picnic</h1>
<table>
<tr><th>Item</th><th>Quantity</th></tr>
%for row in rows:
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    </tr>
%end
</table>