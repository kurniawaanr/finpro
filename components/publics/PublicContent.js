import { Fragment } from "react";

import styled from "styled-components";

//Styling components
const ContentBackground = styled.div`
  position: relative;
  margin-top: 9vh;
  padding: 3vh 1vw;
`;

function PublicContent() {
    return (
        <Fragment>
            <ContentBackground>Test Content</ContentBackground>
        </Fragment>
    );
}

export default PublicContent;