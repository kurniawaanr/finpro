import { Typography, Button } from "antd";
const { Title } = Typography;

import { PlusOutlined } from "@ant-design/icons";

import styled from "styled-components";
import AdminTable from "../general/AdminTable";

//Styling components
const ContentBackground = styled.div`
  position: absolute;
  background-color: white;
  top: 9vh;
  left: 16vw;
  width: 84vw;
  min-height: 91vh;
  padding: 10px;
`;

const LeftColumn = styled.div`
  float: left;
`;

const RightColumn = styled.div`
  float: right;
`;

const MainColumn = styled.div`
  padding: 11vh 1vw;
  padding-bottom: 0;
`;

function AdminContent(props) {
  return (
    <ContentBackground>
      <div>
        <LeftColumn>
          <Title>{props.title}</Title>
        </LeftColumn>
        <RightColumn>
          {props.addButton && (
            <Button
              style={{
                border: "3px solid darkblue",
                padding: "3px 5px",
                borderRadius: "7px",
              }}
              icon={<PlusOutlined />}
            >
              Add New {props.singleWord}
            </Button>
          )}
        </RightColumn>
      </div>
      <MainColumn>
        {props.showTable && (
          <AdminTable columns={props.tableStructure} data={props.tableData} onSetSortedInfo={props.onSetSortedInfo} />
        )}
      </MainColumn>
    </ContentBackground>
  );
}

export default AdminContent;
