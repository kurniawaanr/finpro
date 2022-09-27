import { useRouter } from "next/router";

import { Row, Col, Menu } from "antd";
import styled from "styled-components";

import { profileMenuItems } from "../SystemConfig";

//Styling components
const ProfilePageBox = styled.div`
    padding: 5vh 10vw;
`;

function ProfilePageLayout(props) {
    const router = useRouter();

    const onClick = (e) => {
        console.log("click ", e.key);
        const url = "/profile/" + e.key;
        router.push(url);
    };

    return (
        <ProfilePageBox>
            <Row gutter={16}>
                <Col className="gutter-row" span={8}>
                    <Menu
                        theme="dark"
                        mode="inline"
                        items={profileMenuItems}
                        defaultSelectedKeys={[props.menuKey]}
                        onClick={onClick}
                    />
                </Col>
                <Col className="gutter-row" span={16}>
                    {props.children}
                </Col>
            </Row>
        </ProfilePageBox>
    );
}

export default ProfilePageLayout;