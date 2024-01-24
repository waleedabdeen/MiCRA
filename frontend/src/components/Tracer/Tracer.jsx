import React, { useCallback, useEffect, useState } from "react";
import { Alert, Checkbox, Space, Table } from "antd";
import { isArrayEmpty } from "../../utils/objectUtils";
import { read } from "../../data/restApi";
import Chart from "react-google-charts";

const initialChartData = [["From", "To", "Weight"]];

const Tracer = ({ labels, source }) => {
    const [requirements, setRequirements] = useState();
    const [chartData, setChartData] = useState(initialChartData);
    const [filter, setFilter] = useState([]);

    // const [filter, setFilter] = useState();
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
        let params = { labels: filter };

        read('requirements', params)
            .then(result => {
                let reqs = result.requirements?.map(req => ({
                    id: req.req_id,
                    text: req.req_text,
                    labels: req.label_str,
                    labels_array: req.label
                }));

                setRequirements(reqs);
            })
            .catch(error => console.error(error));
    };

    const handleFilterChanaged = (filter => {
        setFilter(filter);
        fetchRequirements(filter);
    });

    const updateChartData = useCallback(() => {
        if (!isArrayEmpty(requirements) && !isArrayEmpty(labels)) {
            let newData = [...initialChartData];
            for (let j = 0; j < filter.length; j++) {
                let label = filter[j];
                let datapoint = ["Input", label, 1];
                newData.push(datapoint);
            }
            for (let i = 0; i < requirements.length; i++) {
                let req = requirements[i];
                req.labels_array.forEach(l => {
                    if (filter.includes(l)) {
                        // let desc = labels.filter(element => element.label == l)?.desc
                        let datapoint = [l, req.id, 1];
                        newData.push(datapoint);
                    }
                });
            }
            setChartData(newData);
        } else {
            setChartData(initialChartData);
        }
    }, [requirements, filter, labels]);

    useEffect(() => {
        if (!isArrayEmpty(labels)) {
            let labelsIds = labels.map(e => e.label);
            fetchRequirements(labelsIds);
        } else {
            setRequirements([]);
        }

    }, [labels]);

    useEffect(() => {
        updateChartData();
    }, [requirements, filter, updateChartData]);

    const options = {
        height: 500,
        width: 600,
        sankey: {
            node: {
                label: {
                    fontSize: 12,
                }
            }
        }
    };

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
            <Table dataSource={requirements} columns={columns} pagination={{ pageSize: 5 }} />
            {chartData.length === 1 ?
                <div></div>
                :
                <>
                    <Alert
                        message="Visualization"
                        description={'A chart that depict the trace: input text -> labels -> requirements'}
                        type="info"
                        showIcon
                    />
                    <Chart
                        chartType="Sankey"
                        width="100%"
                        height="700px"
                        data={chartData}
                        options={options}
                    />
                </>

            }
        </Space>}
    </>;
};

export default Tracer;