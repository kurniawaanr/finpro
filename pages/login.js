import Head from 'next/head'
import Image from 'next/image';

import styled from 'styled-components';

import 'antd/dist/antd.css';
import { Card, Input, Button, Typography } from 'antd';

const { Title } = Typography;

const Background = styled.div`
    background-color: rgb(19,77,203);
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

const LoginForm = styled.div`
    padding-top: 5vh;
    text-align: left;
`;

const LoginInput = styled(Input)`
    margin-bottom: 2vh;
    border-bottom: 1px solid lightgray;
    &:hover, &:focus{
        border-bottom: 1px solid black;
    }
`


function Login() {
    return (
        <>
            <Head>
                <title>Login to SC SIM</title>
                <meta name="description" content="Login page to enter Startup Campus Sistem Informasi" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Background>
                <LoginCard>
                    <Image src="/images/Startup-Campus-Site-Logo.png" alt="Startup Campus Logo" width={143} height={47} />
                    <Title level={4}>Login to MIS</Title>
                    <LoginForm>
                        Username
                        <LoginInput placeholder="Type your username" bordered={false} />
                        Password
                        <LoginInput placeholder="Type your password" bordered={false} />
                        <Button type='primary' shape='round' block>Login!</Button>
                    </LoginForm>
                </LoginCard>
            </Background>
        </>
    );
}

export default Login;