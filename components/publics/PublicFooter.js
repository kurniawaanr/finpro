import { Fragment } from "react";

import Image from "next/image";

import styled from "styled-components";

import { Typography } from "antd";
const { Title } = Typography;

//Styling components
const FooterBackground = styled.div`
  position: relative;
  padding: 3vh 1vw;
  background-color: darkgray;
  color: black;
  width: 100vw;
  height: 35vh;
`;

const LeftFooter = styled.div`
  float: left;
  margin-left: 2vw;
`;

const RightFooter = styled.div`
  float: right;
  width: 20vw;
`;

const MiddleFooter = styled.div`
   position: absolute;
   left: 50vw;
`;

const ImageBox = styled.div`
`;

const DescriptionBox = styled.div`
    width: 25vw;
`;

const ChannelsBox = styled.div`
    margin-top: 2vh;
`;

const ChannelIcon = styled.span`
    margin-right: 0.5vw;
`;

const LinkedText = styled.a`
    font-size: 1.15vw;
    color: black;
    display: block;
`;


function PublicFooter() {
    return (
        <Fragment>
            <FooterBackground>
                <LeftFooter>
                    <ImageBox>
                        <Image
                            src="/images/Startup-Campus-Site-Logo.png"
                            alt="Startup Campus Logo"
                            width={150}
                            height={40}
                        />
                    </ImageBox>
                    <DescriptionBox>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed laoreet dui nec pulvinar ultricies. Fusce accumsan auctor elit, ac hendrerit justo malesuada ac. Donec faucibus aliquam feugiat. Mauris commodo tellus sed pulvinar convallis.
                    </DescriptionBox>
                    <ChannelsBox>
                        <Title level={4}>Our Channels</Title>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/twitter.png"
                                alt="Twitter Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/instagram.png"
                                alt="Instagram Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/tik-tok.png"
                                alt="Tiktok Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/facebook.png"
                                alt="Facebook Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/linkedin.png"
                                alt="Linkedin Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                        <ChannelIcon>
                            <Image
                                src="/images/icons/youtube.png"
                                alt="Youtube Logo"
                                width={30}
                                height={30}
                            />
                        </ChannelIcon>
                    </ChannelsBox>
                </LeftFooter>
                <MiddleFooter>
                    <LinkedText href="http://www.google.com" target="_blank"> About us</LinkedText>
                    <LinkedText href="http://www.google.com" target="_blank"> Product & services</LinkedText>
                    <LinkedText href="http://www.google.com" target="_blank"> Payment status</LinkedText>
                    <LinkedText href="http://www.google.com" target="_blank"> Track your order</LinkedText>
                    <LinkedText href="http://www.google.com" target="_blank"> Become our seller</LinkedText>
                    <LinkedText href="http://www.google.com" target="_blank"> Contact us</LinkedText>
                </MiddleFooter>
                <RightFooter>
                    <Title level={5}>Our Location</Title>
                    <p>
                        Address -- 123 Street Road, South <br />
                        Jakarta, DKI Jakarta, Indonesia
                    </p>
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d8096018.701773022!2d101.41263544999995!3d-7.775598899999991!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e7a59f8aaddadb7%3A0xdc6b1bc588b24967!2sMSIB%20Kampus%20Merdeka%20Corner!5e0!3m2!1sen!2sde!4v1662321513925!5m2!1sen!2sde" width="200" height="150" style={{border:0}} loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                </RightFooter>
            </FooterBackground>
        </Fragment>
    )
}

export default PublicFooter;