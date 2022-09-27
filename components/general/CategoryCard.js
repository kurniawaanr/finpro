import { Card } from "antd";
import styled from "styled-components";

//Styling components
const CardTitle = styled.div``;
const CardPicture = styled.div`
    text-align: center;
`;

function CategoryCard(props) {
    return (
        <Card>
            <CardTitle>{props.title}</CardTitle>
            <CardPicture><img src={props.image} /></CardPicture>
        </Card>
    );
}

export default CategoryCard;