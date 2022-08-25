import { Fragment } from "react";

import Image from "next/image";
import { useRouter } from "next/router";

import { Menu } from "antd";

import styled from "styled-components";

import { menubarItems } from "../../SystemConfig";

//Styling components
const MenubarBackground = styled.div`
  position: absolute;
  top: 0;
  width: 16vw;
  background-color: rgb(248, 248, 248);
  height: 100vh;
  color: white;
  padding-top: 15px;
  box-shadow: inset -4px 0px 4px #0000000f;
`;

const ImageBox = styled.div`
  margin-left: 2vw;
`;

function AdminMenubar() {
  const router = useRouter();

  const onClick = (e) => {
    console.log("click ", e.key);
    const url = "/admin" + (e.key == "home" ? "" : ("/"+e.key));
    router.push(url);
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
              backgroundColor: "rgb(248, 248, 248)",
              marginTop: "5vh"
          }}
        />
      </MenubarBackground>
    </Fragment>
  );
}

export default AdminMenubar;
