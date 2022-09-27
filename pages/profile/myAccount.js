import { useState, useEffect } from "react";
import { Typography, Divider, Form, Input, Button } from "antd";
import styled from "styled-components";

import PublicLayout from "../../layouts/PublicLayout";
import ProfilePageLayout from "../../layouts/ProfilePageLayout";
import { shippingFormStructure } from "../../SystemConfig";

const { Title, Text } = Typography;
const { TextArea } = Input;

//Styling components
const ProfilePageDivider = styled(Divider)`
    border: 1px solid gray;
`;

const layout = {
    labelCol: {
        span: 3,
    },
    wrapperCol: {
        span: 10,
    },
};

function myAccountPage() {
    const [userName, setUserName] = useState("");
    const [userEmail, setUserEmail] = useState("");
    const [shippingName, setShippingName] = useState("");
    const [shippingTelp, setShippingTelp] = useState("");
    const [shippingAddress, setShippingAddress] = useState("");

    const [form] = Form.useForm();
    let formItems = [];

    useEffect(() => {
        setUserName("John Doe");
        setUserEmail("johndoe@gmail.com");

        form.setFieldsValue({
            name: "William Onnyx",
            phone: "08123456789",
            address: "22, Street Road, South jakarta, DKI Jakarta, 12029"
        });
    });

    const fieldType = (formItem) => {
        const attrs = {
            label: formItem[0],
            name: formItem[1],
        }

        if (formItem[3] != "none") attrs.rules = formItem[3];

        if (formItem[2] == "text") {
            return (
                <Form.Item {...attrs}>
                    <Input />
                </Form.Item>);
        }
        else if (formItem[2] == "multilineText") {
            return (
                <Form.Item {...attrs}>
                    <TextArea />
                </Form.Item>);
        }
    }

    const onFinish = (values) => {
        console.log('Received values of form:', values);
    };

    shippingFormStructure.forEach(formItem => {
        formItems.push(fieldType(formItem));
    })

    return (
        <PublicLayout title="My Account Page">
            <ProfilePageLayout menuKey="myAccount">
                <Title level={3}>General Information</Title>
                <Text strong>Name: {userName} <br /></Text>
                <Text strong>Email: {userEmail} <br /></Text>
                <Text strong>Password: ******** <br /></Text>

                <ProfilePageDivider />
                <Title level={3}>Shipping Address</Title>
                <Form
                    form={form}
                    name="shippingForm"
                    {...layout}
                    onFinish={onFinish}
                >
                    {formItems}
                    <Form.Item>
                        <Button type="primary" htmlType="submit">Save</Button>
                    </Form.Item>
                </Form>
            </ProfilePageLayout>
        </PublicLayout>
    );
}

export default myAccountPage;