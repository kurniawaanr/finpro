import { Fragment } from "react";

import Image from "next/image";

import { Menu } from "antd";
import {
  AppstoreOutlined,
  MailOutlined,
  SettingOutlined,
} from "@ant-design/icons";

import styled from "styled-components";

//Styling components
const MenubarBackground = styled.div`
  position: absolute;
  top: 0;
  width: 256px;
  background-color: darkgray;
  height: 100vh;
  color: white;
  padding-top: 15px;
  box-shadow: 8px 0 8px -4px lightslategray;
`;

const ImageBox = styled.div`
  margin-left: 2vw;
`;

function getItem(label, key, icon, children, type) {
  return {
    key,
    icon,
    children,
    label,
    type,
  };
}

const menubarItems = [
  getItem("Navigation One", "sub1", <MailOutlined />, [
    getItem(
      "Item 1",
      "g1",
      null,
      [getItem("Option 1", "1"), getItem("Option 2", "2")],
      "group"
    ),
    getItem(
      "Item 2",
      "g2",
      null,
      [getItem("Option 3", "3"), getItem("Option 4", "4")],
      "group"
    ),
  ]),
  getItem("Navigation Two", "sub2", <AppstoreOutlined />, [
    getItem("Option 5", "5"),
    getItem("Option 6", "6"),
    getItem("Submenu", "sub3", null, [
      getItem("Option 7", "7"),
      getItem("Option 8", "8"),
    ]),
  ]),
  getItem("Navigation Three", "sub4", <SettingOutlined />, [
    getItem("Option 9", "9"),
    getItem("Option 10", "10"),
    getItem("Option 11", "11"),
    getItem("Option 12", "12"),
  ]),
];

function AdminMenubar() {
  const onClick = (e) => {
    console.log("click ", e);
  };

  return (
    <Fragment>
      <MenubarBackground>
        <ImageBox>
          <Image
            src="/images/Startup-Campus-Site-Logo.png"
            alt="Startup Campus Logo"
            width={170}
            height={40}
          />
        </ImageBox>
        <Menu
          onClick={onClick}
          id="MenuBarMenu"
          mode="inline"
          items={menubarItems}
          style={{
              backgroundColor: "darkgray",
              marginTop: "5vh"
          }}
        />
      </MenubarBackground>
    </Fragment>
  );
}

export default AdminMenubar;
