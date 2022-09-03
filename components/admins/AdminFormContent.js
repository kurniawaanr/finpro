import { useEffect, useState } from "react";

import { Typography, Form, Input, InputNumber, Select, Upload, Button } from "antd";
import { PlusOutlined } from '@ant-design/icons';
const { Title } = Typography;
const { TextArea } = Input;
const { Option } = Select;

import { useRouter } from "next/router";

import styled from "styled-components";

import { productFormStructure } from "../../SystemConfig";

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
  clear: left;
`;

const MainColumn = styled.div`
  padding: 11vh 1vw;
  padding-bottom: 0;
`;

const ButtonSubmit = styled(Button)`
    margin-left: 6vw;
    width: 10vw;
`;

const layout = {
    labelCol: {
        span: 3,
    },
    wrapperCol: {
        span: 10,
    },
};


function AdminFormContent(props) {
    const router = useRouter();
    const linkName = router.route.split('/')[2];
    const formType = router.query.productId == 'add' ? 'Add' : 'Edit'
    const buttonText = router.query.productId == 'add' ? 'Create' : 'Edit'
    let formItems = [];

    const [form] = Form.useForm();
    const [fileList, setFileList] = useState([
        {
            uid: '-1',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
        },
        {
            uid: '-2',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
        },
        {
            uid: '-3',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
        },
        {
            uid: '-4',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
        },
        {
            uid: '-xxx',
            percent: 50,
            name: 'image.png',
            status: 'uploading',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
        },
        {
            uid: '-5',
            name: 'image.png',
            status: 'error',
        },
    ]);

    useEffect(() => {
        if (router.query.productId != 'add') {
            console.log("modify disini");
            form.setFieldsValue({
                name: "William Onnyx",
                description: "Hello my name is William",
                price: 20000,
                category: "Pakaian Pria",
                brand: "Boss",
                condition: "New"
            });
        }
    }, [form]);

    const capitalizeFirstLetter = (word) => {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }

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
        else if (formItem[2] == "number") {
            return (
                <Form.Item {...attrs}>
                    <InputNumber />
                </Form.Item>);
        }
        else if (formItem[2] == "multilineText") {
            return (
                <Form.Item {...attrs}>
                    <TextArea />
                </Form.Item>);
        }
        else if (formItem[2] == "selectBox") {
            return (
                <Form.Item {...attrs}>
                    <Select placeholder={`Please choose ${linkName} ${formItem[1]}`}>
                        {formItem[4].map(item => {
                            return (<Option value={item}>{capitalizeFirstLetter(item)}</Option>)
                        })}
                    </Select>
                </Form.Item>);
        }
        else if (formItem[2] == "uploadImage") {
            return (
                <Form.Item {...attrs}>
                    <Upload 
                        listType="picture-card" 
                        fileList={fileList}
                        onChange={handleChangePicture}
                    >
                        <div>
                            <PlusOutlined />
                            <div style={{ marginTop: 8 }}>Upload</div>
                        </div>
                    </Upload>
                </Form.Item>);
        }
    }

    const onFinish = (values) => {
        console.log('Received values of form:', values);
    };

    const handleChangePicture = ({ fileList: newFileList }) => setFileList(newFileList);



    if (linkName == "products") {
        productFormStructure.forEach(formItem => {
            formItems.push(fieldType(formItem));
        })
    }

    return (
        <ContentBackground>
            <div>
                <LeftColumn>
                    <Title>{capitalizeFirstLetter(linkName)} {formType} Form</Title>
                </LeftColumn>
                <MainColumn>
                    <Form
                        form={form}
                        name="adminForm"
                        {...layout}
                        onFinish={onFinish}
                    >
                        {formItems}
                        <Form.Item>
                            <ButtonSubmit type="primary" htmlType="submit">{buttonText}</ButtonSubmit>
                        </Form.Item>
                    </Form>
                </MainColumn>
            </div>
        </ContentBackground>
    );
}

export default AdminFormContent;