import React, { useState } from "react";
import { Button, Form, Input, Select, Space, Checkbox, Alert } from "antd";
import { read, write } from "../../data/restApi";

const ClassifierForm = ({ onComplete, onTextChange }) => {
    const { TextArea } = Input;
    const [artifactForm] = Form.useForm();
    const [labelsForm] = Form.useForm();
    const [labels, setLabels] = useState();
    const [loading, setLoading] = useState(false);
    const [saved, setSaved] = useState(false);

    const onFinish = (e) => {
        setLabels();
        setLoading(true);
        read('classification', { 'text': e.requirement })
            .then(result => {
                setLoading(false);
                setLabels(result.labels.map(e => ({
                    value: e.label, label: `${e.label}. ${e.desc} [${e.score?.toFixed(2)}]`
                })))
            })
            .catch(error => {
                console.error(error);
                setLoading(false);
            });
    };

    const onFinishFailed = ({ values, errorFields }) => {
        console.error(values);
        console.error(errorFields);
    };

    const onSave = (e) => {
        const bodyParams = {
            text: artifactForm.getFieldValue('text'),
            type: artifactForm.getFieldValue('type'),
            labels: e.truelabels
        }

        console.log(bodyParams)

        setLoading(true);
        write('artifacts', undefined, bodyParams)
            .then(result => {
                setLoading(false);
                setSaved(true)
                console.log(result);
            })
            .catch(error => {
                console.error(error);
                setLoading(false);
                setSaved(false)
            });

        console.log(e.truelabels)
    };

    const onSaveFailed = ({ values, errorFields }) => {
        console.error(values);
        console.error(errorFields);
    };



    return <Space direction="vertical" style={{ width: '100%' }}>


        <h3>Artifact Data</h3>
        <Form
            size="large"
            form={artifactForm}
            layout={"vertical"}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            style={{ maxWidth: 1000 }}
        >
            <Form.Item name="type" label="Type">
                <Select
                    // initialvalue="BUC"
                    style={{ width: 120 }}
                    options={[
                        { value: 'BUC', label: 'BUC' },
                        { value: 'GPR', label: 'GPR' },
                        { value: 'TC', label: 'TC' }
                    ]}
                />
            </Form.Item>
            <Form.Item name="text" label="Text">
                <TextArea placeholder="enter a text to classify" maxLength={1000} rows={4} />
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
                    <h3>Suggested Labels</h3>
                    <Form
                        size="large"
                        form={labelsForm}
                        onFinish={onSave}
                        onFinishFailed={onSaveFailed}
                    >
                        <Form.Item name={'truelabels'}>
                            <Checkbox.Group
                                options={labels}
                                onChange={(e) => console.log(e)}
                            />
                        </Form.Item>
                        <Form.Item>
                            <Button type="primary" htmlType="submit" loading={loading}>
                                Save
                            </Button>
                        </Form.Item>
                    </Form>
                </>
            }
            {
                saved &&

                <Alert
                    message="Link Saved"
                    type="info"
                    showIcon
                />
            }
        </>
    </Space>
};


export default ClassifierForm;