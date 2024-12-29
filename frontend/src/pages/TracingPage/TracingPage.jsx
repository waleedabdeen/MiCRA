import { useState } from 'react';
import { Steps } from 'antd';
import { Button, Form, Select, Checkbox, Table } from "antd";
import { read } from "../../data/restApi";
import Tracer from "../../components/Tracer/Tracer"

const TracingPage = () => {
  const [current, setCurrent] = useState(0);
  const [sourceType, setSourceType] = useState();
  const [source, setSource] = useState();
  const [sourcesOptions, setSourcesOptions] = useState([]);
  const [records, setRecords] = useState([]);
  const [targets, setTargets] = useState([]);
  const [targetType, setTargetType] = useState();
  const [artifactForm] = Form.useForm()

  const onTextChange = (changedValues, allData) => {
    if (changedValues.sourceType) {
      setSourceType(changedValues.sourceType)
      read('artifacts', { 'type': changedValues.sourceType })
        .then(result => {
          console.log(result)

          let options = result.map(r => (
            {
              key: r.id,
              value: r.id,
              label: r.id
            }
          ));
          setSourcesOptions(options);
          setRecords(result);
          setSource();
        })
        .catch(console.error)
    }
    if (changedValues.source) {
      setSource(changedValues.source);
    }
  };

  const onStepChange = (value) => {
    setCurrent(value);
  };


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
        values.map(e => <div>[{e}]</div>)
      )
    },
  ];

  const nextStep = () => {

  };

  return (
    <Steps
      current={current}
      onChange={onStepChange}
      direction="vertical"
      items={[
        {
          title: 'Step 1: Select Artifacts',
          description: (
            <>
              <Form
                form={artifactForm}
                layout={"inline"}
                // onFinish={onFinish}
                // onFinishFailed={onFinishFailed}
                onValuesChange={onTextChange}
                style={{ maxWidth: 1000 }}
              >
                <Form.Item name="sourceType" label="Source type">
                  <Select
                    value={sourceType}
                    style={{ width: 120 }}
                    options={[
                      { value: 'BUC', label: 'BUC' },
                      { value: 'GPR', label: 'GPR' },
                      { value: 'TC', label: 'TC' }
                    ]}
                  />
                </Form.Item>
                <Form.Item name="source" label="Source">
                  <Select
                    value={source}
                    style={{ width: 120 }}
                    options={sourcesOptions}
                  />
                </Form.Item>
              </Form>
              <p>
                {source && records && records.find(e => e.id == source)?.text}
              </p>
            </>
          )
        },
        {
          title: 'Step 2: Related Artifacts',
          description: (<>
            <Tracer labels={records.find(e => e.id == source)?.labels} />
          </>)
        },

      ]}
    />


  );
}

export default TracingPage;
