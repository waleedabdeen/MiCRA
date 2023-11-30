import React, { useState } from "react";
import { Button, Form, Input, List, Divider, Avatar, Steps, Alert, Space } from "antd";
import { read } from "../../data/restApi";


const ClassifierForm = ({ onComplete, onTextChange }) => {
    const { TextArea } = Input;
    const [form] = Form.useForm();

    const [labels, setLabels] = useState();
    const [loading, setLoading] = useState(false);

    const onFinish = (e) => {
        setLabels();
        setLoading(true);
        read('classification', { 'text': e.requirement })
            .then(result => {
                setLoading(false);
                setLabels(result.labels)
                onComplete(e.requirement, result.labels);
            })
            .catch(error => {
                console.error(error);
                setLoading(false);
            });
    };

    const onFinishFailed = ({ values, errorFields }) => {
        console.log(values);
        console.log(errorFields);
    };

    return <Space direction="vertical" style={{ width: '100%' }}>
        <Alert
            message="Enter requirement text"
            description="Enter requirement text in the input box to classify (max 1000 character)."
            type="info"
            showIcon
        />
        <Form
            size="large"
            form={form}
            layout={"vertical"}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            onValuesChange={onTextChange}
            style={{ maxWidth: 1000 }}
        >
            <Form.Item name="requirement" label="Requirement">
                <TextArea placeholder="enter a requirement to classify" maxLength={1000} rows={4} />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                    Classify
                </Button>
            </Form.Item>
        </Form>

        <>
            {labels &&
                <>
                    <Divider orientation="left">Labels</Divider>
                    <List
                        className="white-bg"
                        itemLayout="horizontal"
                        bordered
                        dataSource={labels}
                        renderItem={(item, index) => (
                            <List.Item>
                                <List.Item.Meta
                                    avatar={index + 1}
                                    title={item.desc}
                                    description={item.label + ' - ' + item.score?.toFixed(2)}
                                />
                            </List.Item>
                        )}
                    />
                </>
            }
        </>
    </Space>
};


export default ClassifierForm;