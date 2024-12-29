import React, { useCallback, useEffect, useState } from "react";
import { Alert, Checkbox, Select, Space, Table } from "antd";
import { isArrayEmpty } from "../../utils/objectUtils";
import { read } from "../../data/restApi";
import Chart from "react-google-charts";

const initialChartData = [["From", "To", "Weight"]];

const Tracer = ({ labels, source }) => {
    const [requirements, setRequirements] = useState();
    const [targetType, setTargetType] = useState();
    const [chartData, setChartData] = useState(initialChartData);
    const [selectedLabels, setSelectedLabels] = useState(labels);

    // const [filter, setFilter] = useState();
    const columns = [
        {
            title: 'Id',
            dataIndex: 'id',
            key: 'id',
            width: '10%'
        },
        {
            title: 'Type',
            dataIndex: 'type',
            key: 'type',
            width: '10%'
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
                values.map(e => <div>[{e.label} - {e.label_name}]</div>)
            )
        },
    ];


    const fetchRequirements = (labelsIds, targetType) => {
        let params = { type: targetType, labels: labelsIds };

        read('artifacts', params)
            .then(result => {
                let reqs = result.map(req => ({
                    key: req.id,
                    id: req.id,
                    text: req.text,
                    type: req.type,
                    label_str: req.label_str,
                    labels: req.labels
                }));

                console.log(result)
                setRequirements(reqs);
            })
            .catch(error => console.error(error));
    };

    // const updateChartData = useCallback(() => {
    //     if (!isArrayEmpty(requirements) && !isArrayEmpty(labels)) {
    //         let newData = [...initialChartData];
    //         for (let j = 0; j < labels.length; j++) {
    //             let label = labels[j];
    //             let datapoint = ["Input", label, 1];
    //             newData.push(datapoint);
    //         }
    //         for (let i = 0; i < requirements.length; i++) {
    //             let req = requirements[i];
    //             req.labels_array.forEach(l => {
    //                 if (labels.includes(l)) {
    //                     // let desc = labels.filter(element => element.label == l)?.desc
    //                     let datapoint = [l, req.id, 1];
    //                     newData.push(datapoint);
    //                 }
    //             });
    //         }
    //         setChartData(newData);
    //     } else {
    //         setChartData(initialChartData);
    //     }
    // }, [requirements, labels, labels]);

    useEffect(() => {
        if (!isArrayEmpty(selectedLabels)) {
            fetchRequirements(selectedLabels, targetType);
        } else {
            setRequirements([]);
        }

    }, [selectedLabels, targetType]);

    // useEffect(() => {
    //     updateChartData();
    // }, [requirements, labels, updateChartData]);

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
            <Select
                value={targetType}
                onChange={(t) => {
                    setTargetType(t)
                }}
                style={{ width: 120 }}
                options={[
                    { value: 'BUC', label: 'BUC' },
                    { value: 'GPR', label: 'GPR' },
                    { value: 'TC', label: 'TC' }
                ]}
            />

            <Checkbox.Group
                defaultValue={labels.map(e => e.label)}
                options={labels?.map(element => {
                    return { label: `${element.label} - ${element.label_name}`, value: element.label }
                })}
                onChange={(e) => {
                    setSelectedLabels(e)
                    console.log(e)
                }}
            />
            <Table dataSource={requirements} columns={columns} pagination={{ pageSize: 5 }} />
            {/* {chartData.length === 1 ?
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

            } */}
        </Space>}
    </>;
};

export default Tracer;