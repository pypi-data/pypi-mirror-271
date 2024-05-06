use pyo3::prelude::*;
use pyo3::types::PyBytes;

fn encode_gene_byte(gene: u8) -> u8 {
    match gene {
        b'A' => 0b00,
        b'T' => 0b01,
        b'C' => 0b10,
        b'G' => 0b11,
        _ => panic!("Invalid gene: {}", gene as char),
    }
}


#[pyfunction]
fn encode_gene(py: Python, gene_sequence: &str) ->PyObject  {
    let padding_gene = if gene_sequence.ends_with('A') { b'T' } else { b'A' };

    let mut encoded: Vec<u8> = Vec::new();

    // 将字符串转换为字节数组
    let bytes = gene_sequence.as_bytes();

    // 每次处理 4 个基因
    for chunk in bytes.chunks(4) {
        let padding_len = 4 - chunk.len();
        let mut byte = 0u8;

        if padding_len > 0 {
            let mut padded_chunk = Vec::from(chunk);
            padded_chunk.extend(std::iter::repeat(padding_gene).take(padding_len));
            for (i, gene) in padded_chunk.iter_mut().enumerate(){
                byte |= encode_gene_byte(*gene) << (i * 2);
            }
        }else{
            for (i, &gene) in chunk.iter().enumerate() {
                byte |= encode_gene_byte(gene) << (i * 2);
            }
        }
        encoded.push(byte);
    }

    // 补充一个byte作为标志
    encoded.push(padding_gene-b'A');
    // Ok(encoded)
    PyBytes::new(py, &encoded).into()
}

// 解码函数
#[pyfunction]
fn decode_gene(encoded: &[u8]) -> PyResult<String> {
    let mut decoded = String::new();
    let padding_gene = encoded[encoded.len() - 1] + b'A'; // 获取填充基因

    for &byte in encoded[..encoded.len() - 1].iter() { // 跳过最后 4 个填充基因
        for i in 0..4 {
            decoded.push(match (byte >> (i * 2)) & 0b11 {
                0b00 => 'A',
                0b01 => 'T',
                0b10 => 'C',
                0b11 => 'G',
                _ => panic!("Invalid encoding"),
            });
        }
    }

    // 移除末尾的填充基因
    while decoded.ends_with(padding_gene as char) {
        decoded.pop();
    }

    Ok(decoded)
}

#[pyfunction]
fn encode_u40(py: Python,text: &str) -> PyObject {
    // u40的取值范围是 0~1_099_511_627_775, 这里的编码范围是 999_999_999_999
    // 超过 1_000_000_000_000 表示为特殊位，错过几位表示前一个值取多少个有效数值，非末尾，还需要添加上小数标点。
    // 1_000_000_000_000 仅代表小数点位，不影响前值。
    // 超过 1_000_000_000_000 - 1_000_000_000_999 表示为小数点位，当前点代表小数点，零头代表前值的有效位数。
    // 超过 1_000_000_001_000 - 1_000_000_001_100 表示为结尾，当前没有值，零头 - 100 代表前值的有效位数。
    // 1_099_511_627_775

    // const MAX: u64 = ((1 as u64) << 40) - 1;
    // const NUMBER_FLAG_LTE: u64 = 999_999_999_999;
    const POINT_FLAG: u64 = 1_000_000_000_000;
    // const POINT_UPPER_GTE: u64 = 1_000_000_000_001;
    // const POINT_UPPER_LTE: u64 = 1_000_000_000_999;
    const END_UPPER_GTE: u64 = 1_000_000_001_000;
    // const END_UPPER_LTE: u64 = 1_000_000_001_100;
    // assert!(value <= $name::MAX.0 && value >= $name::MIN.0);

    let mut result = Vec::new();
    // let mut buffer = [0u8; 5];
    // let mut count = 0;

    let chunk_size: usize = 12;
    let mut start: usize = 0;
    let mut end: usize = 0;

    for (index, c) in text.chars().enumerate() {
        // point
        if c == '.' {
            let mut point_value: Vec<u8>;
            if end - start == 0 {
                // pervious value handled
                // task
                // 1. save point
                point_value = POINT_FLAG.to_be_bytes().to_vec();
            } else {
                // task
                // 1. save pervious value
                // 2. save point
                let numeric_value: u64 = text[start..end].to_string().parse().unwrap();
                let mut number_bit_vec = numeric_value.to_be_bytes().to_vec();
                number_bit_vec.drain(0..3);
                result.extend_from_slice(&number_bit_vec);

                point_value = ((end - start) as u64 + POINT_FLAG).to_be_bytes().to_vec();
            }
            point_value.drain(0..3);
            result.extend_from_slice(&point_value);

            // move cur after point
            end = index + 1;
            start = index + 1;
        } else {
            // handle before
            if end - start == chunk_size {
                let numeric_value: u64 = text[start..end].to_string().parse().unwrap();
                let mut vv = numeric_value.to_be_bytes().to_vec();
                vv.drain(0..3);
                result.extend_from_slice(&vv);
                // println!("numeric_value: {}",numeric_value);
                start = index
            }
            end = index + 1;
        }
    }
    // string end
    if end > start {
        let numeric_value: u64 = text[start..end].to_string().parse().unwrap();
        let mut number_bit_vec = numeric_value.to_be_bytes().to_vec();
        number_bit_vec.drain(0..3);
        result.extend_from_slice(&number_bit_vec);
        // println!("numeric_value: {}",numeric_value);

        let mut point_value: Vec<u8> = ((end - start) as u64 + END_UPPER_GTE).to_be_bytes().to_vec();
        point_value.drain(0..3);
        result.extend_from_slice(&point_value);
    }
    
    PyBytes::new(py, &result).into()
}

#[pyfunction]
fn decode_u40(encoded: &[u8]) -> String {
    
    // const MAX: u64 = ((1 as u64) << 40) - 1;
    const NUMBER_FLAG_LTE: u64 = 999_999_999_999;
    const POINT_FLAG: u64 = 1_000_000_000_000;
    // const POINT_UPPER_GTE: u64 = 1_000_000_000_001;
    const POINT_UPPER_LTE: u64 = 1_000_000_000_999;
    const END_UPPER_GTE: u64 = 1_000_000_001_000;
    const END_UPPER_LTE: u64 = 1_000_000_001_100;
    
    let mut decoded = String::new();
    let mut last_num: u64 = 0;
    for (i, chunk) in encoded.chunks(5).enumerate() {
        let mut bytes = [0u8; 8];
        bytes[3..8].copy_from_slice(&chunk); // 将 Vec<u8> 复制到数组的低 5 个字节
        let current_num = u64::from_be_bytes(bytes);

        // 开始节点，已经刚处理完小数点
        if i == 0 {
            last_num = current_num;
            continue;
        }

        if current_num <= NUMBER_FLAG_LTE {
            if last_num <= NUMBER_FLAG_LTE {
                // ex. 12
                let formatted = format!("{:012}", last_num);
                decoded.push_str(formatted.as_str());
            } else if last_num <= POINT_UPPER_LTE {
                // ex. .1
                decoded.push('.');
            }
        } else if current_num == POINT_FLAG {
            // ex *.
            decoded.push('.');
        } else if current_num <= POINT_UPPER_LTE{
            // ex 1.
            let digital: usize = (current_num - POINT_FLAG) as usize;
            // println!("digital: {}", digital);
            let formatted = format!("{:0digital$}", last_num,);
            decoded.push_str(formatted.as_str());
        } else if current_num <= END_UPPER_LTE{
            // ex 1. EOF
            let digital: usize = (current_num - END_UPPER_GTE) as usize;
            // println!("digital: {}", digital);
            let formatted = format!("{:0digital$}", last_num,);
            decoded.push_str(formatted.as_str());
        } 
        last_num = current_num;
    }

    if last_num >= POINT_FLAG && last_num <=POINT_UPPER_LTE{
        decoded.push('.');
    }

    decoded
}


/// A Python module implemented in Rust.
#[pymodule]
fn data_encode_tool(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encode_gene, m)?)?;
    m.add_function(wrap_pyfunction!(decode_gene, m)?)?;
    m.add_function(wrap_pyfunction!(encode_u40, m)?)?;
    m.add_function(wrap_pyfunction!(decode_u40, m)?)?;
    Ok(())
}

