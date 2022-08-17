import { Fragment, useEffect, useCallback } from "react";

import Image from "next/image";
import { useRouter } from "next/router";

import styled from "styled-components";

import "antd/dist/antd.css";
import { Card, Input, Button, Typography, Form, Checkbox } from "antd";
import { EyeInvisibleOutlined, EyeTwoTone } from "@ant-design/icons";

//Import Redux
import { useDispatch, useSelector } from "react-redux";
import { selectIsLoggedIn, loginHandler } from "../store/features/userReducer";

//Extending ANTD import
const { Title } = Typography;

//Import Components
import WebsiteHead from "../components/WebsiteHead";

//Styling Components
const Background = styled.div`
  background-color: rgb(19, 77, 203);
  width: 100vw;
  height: 100vh;
`;

const LoginCard = styled(Card)`
  position: relative;
  top: 15%;
  left: 40%;
  padding: 10px;

  width: 20vw;
  height: 30vw;
  border-radius: 10px;
  text-align: center;
`;

const LoginForm = styled(Form)`
  padding-top: 5vh;
  text-align: left;
`;

const LoginInput = styled(Input)`
  margin-bottom: 2vh;
  border-bottom: 1px solid lightgray;
  &:hover,
  &:focus {
    border-bottom: 1px solid black;
  }
`;

const LoginInputPassword = styled(Input.Password)`
  border-bottom: 1px solid lightgray;
  &:hover,
  &:focus {
    border-bottom: 1px solid black;
  }
`;

const ForgetPasswordDiv = styled.div`
  text-align: center;
`;

function Login() {
  const dispatch = useDispatch();
  const selector = useSelector;
  const router = useRouter();

  const isUserLoggedIn = selector(selectIsLoggedIn);

  //useEffect if the user already login or not - if remember me so get from localstorage
  useEffect(()=>{
    if(isUserLoggedIn){
      router.push('/admin');
    }
  });

  const onFinish = (values) => { 
    console.log("Success:", values);
    dispatch(loginHandler({ username: values.username, remember: values.remember }));
    router.push('/admin');
  };

  const forgetPasswordHandler = () => {
    console.log("Forget Password");
  };

  return (
    <Fragment>
      <WebsiteHead
        title="Login to SC SIM"
        desc="Login page to enter Startup Campus Sistem Informasi"
      />
      <Background>
        <LoginCard>
          <Image
            src="/images/Startup-Campus-Site-Logo.png"
            alt="Startup Campus Logo"
            width={143}
            height={47}
          />
          <Title level={4}>Login to MIS</Title>
          <LoginForm name="login form" onFinish={onFinish}>
            Username
            <Form.Item
              name="username"
              rules={[
                {
                  required: true,
                  message: "Please input your username!",
                },
              ]}
            >
              <LoginInput placeholder="Type your username" bordered={false} />
            </Form.Item>
            Password
            <Form.Item
              name="password"
              rules={[
                {
                  required: true,
                  message: "Please input your password!",
                },
              ]}
            >
              <LoginInputPassword
                placeholder="Type your password"
                bordered={false}
                iconRender={(visible) =>
                  visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />
                }
              />
            </Form.Item>
            <Form.Item name="remember" valuePropName="checked">
              <Checkbox>Remember me</Checkbox>
            </Form.Item>
            <Form.Item>
              <Button type="primary" shape="round" block htmlType="submit">
                Login
              </Button>
              <ForgetPasswordDiv>
                <a onClick={forgetPasswordHandler}>Forget Password?</a>
              </ForgetPasswordDiv>
            </Form.Item>
          </LoginForm>
        </LoginCard>
      </Background>
    </Fragment>
  );
}

export default Login;
