import { Alert, Button, Select, Space } from "antd";
import { useEffect, useState } from "react";
import { isArrayEmpty } from "../../utils/objectUtils";



const LabelsSelector = ({ labels, onComplete }) => {
    const [selected, setSelected] = useState([]);

    const handleChange = (values) => {
        setSelected(values);
    };

    const handleNext = () => {
        onComplete(labels.filter(e => selected.includes(e.label)));
    };

    useEffect(() => {
        setSelected([]);
    }, [labels]);

    return <>
        {!isArrayEmpty(labels) &&
            <Space direction="vertical" style={{ width: '100%' }}>
                <Alert
                    message="Select the correct labels"
                    description="Select the labels that fits the requirement text from the dropdown menu. Click next when you are done."
                    type="info"
                    showIcon
                />
                <Select
                    mode="multiple"
                    allowClear
                    style={{ width: '100%' }}
                    placeholder="Please select"
                    onChange={handleChange}
                    options={labels?.map(element => {
                        return { label: element.label + " - " + element.desc, value: element.label }
                    })}
                    value={selected}
                />
                <Button size="large" type='primary' onClick={handleNext}>Next</Button>
            </Space>
        }
    </>
};

export default LabelsSelector;