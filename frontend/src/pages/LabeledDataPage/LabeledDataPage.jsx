import { Button, Form, Select, Space, Table } from "antd";
import { useCallback, useEffect, useMemo, useState } from "react";
import { read } from "../../data/restApi";
import { useForm } from "antd/es/form/Form";

const LabeledDataPage = () => {
    const [requirements, setRequirements] = useState();
    const [data, setData] = useState({ cs: 'SB11', dimension: 'Byggdelar' });
    const [form] = useForm();

    const columns = [
        {
            title: 'Id',
            dataIndex: 'id',
            key: 'id',
            width: '15%'
        },
        {
            title: 'Text',
            dataIndex: 'text',
            key: 'text',
        },
        {
            title: 'Labels',
            dataIndex: 'labels',
            key: 'labels',
            width: '20%',
            render: (values) => (
                values.map(e => <div>[{e}]</div>)
            )
        },
    ];

    const css = [{
        key: "sb11",
        label: "SB11",
        value: "SB11"
    },
    {
        key: "coclass",
        label: "CoClass",
        value: "CoClass"
    }];

    const dimensions = {
        "SB11": [
            {
                key: "byggdelar",
                label: "Byggdelar",
                value: "Byggdelar"
            },
            {
                key: "alternativtabell",
                label: "Alternativtabell",
                value: "Alternativtabell"
            },
            {
                key: "landskapsinformation",
                label: "Landskapsinformation",
                value: "Landskapsinformation"
            }
        ],
        "CoClass": [
            {
                key: "Tillgångssystem",
                label: "Tillgångssystem",
                value: "Tillgångssystem"
            },
            {
                key: "Konstruktiva-system",
                label: "Konstruktiva system",
                value: "Konstruktiva-system"
            },
            {
                key: "Grundfunktioner-och-Komponenter",
                label: "Grundfunktioner och Komponenter",
                value: "Grundfunktioner-och-Komponenter"
            }
        ]
    }

    const onTextChange = (changedValues, allData) => {
        if (changedValues.cs) {
            allData.dimension = dimensions[changedValues.cs][0].value;
            form.setFieldValue('dimension', allData.dimension);
        }
        setData(allData);
    };

    const fetchRequirements = useCallback(() => {
        read('requirements', data)
            .then(result => {
                let reqs = result.requirements?.map(req => {
                    let labels = [];
                    req.label.forEach((label, index) => {
                        labels.push(`${label}: ${req.label_name[index]}.`);
                    });
                    return {
                        id: req.req_id,
                        text: req.req_text,
                        labels: labels
                    }
                });

                setRequirements(reqs);
            })
            .catch(error => console.error(error));
    }, [data]);

    useEffect(() => {
        fetchRequirements();
    }, [data]);

    return <Space direction="vertical">
        <h2>Labeld Data</h2>
        <Form
            form={form}
            layout={"inline"}
            initialValues={data}
            onValuesChange={onTextChange}>
            <Form.Item name='cs'>
                <Select options={css} />
            </Form.Item>
            <Form.Item name='dimension'>
                <Select options={dimensions[data.cs]} />
            </Form.Item>
        </Form>
        <Table dataSource={requirements} columns={columns} />;
    </Space>
};

export default LabeledDataPage;