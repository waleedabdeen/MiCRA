import React, { useEffect, useState } from "react";
import { Alert, Checkbox, Space, Table } from "antd";
import { isArrayEmpty } from "../../utils/objectUtils";
import { read } from "../../data/restApi";


const Tracer = ({ labels, source }) => {
    const [requirements, setRequirements] = useState();
    const [filter, setFilter] = useState();
    const columns = [
        {
            title: 'Id',
            dataIndex: 'id',
            key: 'id',
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
        },
    ];


    const fetchRequirements = (filter) => {
        console.log(filter);
        let params = { labels: filter };

        read('requirements', params)
            .then(result => {
                let reqs = result.requirements?.map(req => ({
                    id: req.req_id,
                    text: req.req_text,
                    labels: req.label_str
                }));

                setRequirements(reqs);
            })
            .catch(error => console.error(error));
    };

    const handleFilterChanaged = (filter => {
        setFilter(filter);
        fetchRequirements(filter);
    });

    useEffect(() => {
        if (!isArrayEmpty(labels)) {
            let labelsIds = labels.map(e => e.label);
            setFilter(labelsIds);
            fetchRequirements(labelsIds);
        } else {
            setFilter([]);
            setRequirements([]);
        }

    }, [labels]);

    return <>
        {!isArrayEmpty(labels) && <Space direction="vertical" style={{ width: '100%' }}>
            <Alert
                message="Trace to other requirements"
                description={`Source requirement: ${source}`}
                type="info"
                showIcon
            />
            <Checkbox.Group
                defaultValue={labels.map(e => e.label)}
                options={labels?.map(element => {
                    return { label: `${element.label} - ${element.desc}`, value: element.label }
                })}
                onChange={handleFilterChanaged} />
            {/* <Button
                type="primary"
                size="large"
                onClick={() => fetchRequirements(filter)}>Trace</Button> */}
            <Table dataSource={requirements} columns={columns} />;
        </Space>}
    </>;
};

export default Tracer;