use tiny_keccak::{CShake, Hasher, Xof};

#[test]
fn test_cshake128_one() {
    let input = b"\x00\x01\x02\x03";
    let mut output = [0u8; 32];
    let name = b"";
    let custom = b"Email Signature";
    let expected = b"\
        \xC1\xC3\x69\x25\xB6\x40\x9A\x04\xF1\xB5\x04\xFC\xBC\xA9\xD8\x2B\
        \x40\x17\x27\x7C\xB5\xED\x2B\x20\x65\xFC\x1D\x38\x14\xD5\xAA\xF5\
    ";

    let mut cshake = CShake::v128(name, custom);
    cshake.update(input);
    cshake.finalize(&mut output);
    assert_eq!(expected, &output);
}

#[test]
fn test_cshake128_two() {
    let input = b"\
        \x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\
        \x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F\
        \x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F\
        \x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F\
        \x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F\
        \x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F\
        \x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F\
        \x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F\
        \x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F\
        \x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F\
        \xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF\
        \xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF\
        \xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\
    ";
    let mut output = [0u8; 32];
    let name = b"";
    let custom = b"Email Signature";
    let expected = b"\
        \xC5\x22\x1D\x50\xE4\xF8\x22\xD9\x6A\x2E\x88\x81\xA9\x61\x42\x0F\
        \x29\x4B\x7B\x24\xFE\x3D\x20\x94\xBA\xED\x2C\x65\x24\xCC\x16\x6B\
    ";

    let mut cshake = CShake::v128(name, custom);
    cshake.update(input);
    cshake.finalize(&mut output);
    assert_eq!(expected, &output);
}

#[test]
fn test_cshake256_one() {
    let input = b"\x00\x01\x02\x03";
    let mut output = [0u8; 64];
    let name = b"";
    let custom = b"Email Signature";
    let expected = b"\
        \xD0\x08\x82\x8E\x2B\x80\xAC\x9D\x22\x18\xFF\xEE\x1D\x07\x0C\x48\
        \xB8\xE4\xC8\x7B\xFF\x32\xC9\x69\x9D\x5B\x68\x96\xEE\xE0\xED\xD1\
        \x64\x02\x0E\x2B\xE0\x56\x08\x58\xD9\xC0\x0C\x03\x7E\x34\xA9\x69\
        \x37\xC5\x61\xA7\x4C\x41\x2B\xB4\xC7\x46\x46\x95\x27\x28\x1C\x8C\
    ";

    let mut cshake = CShake::v256(name, custom);
    cshake.update(input);
    cshake.finalize(&mut output);
    assert_eq!(expected as &[u8], &output as &[u8]);
}

#[test]
fn test_cshake256_two() {
    let input = b"\
        \x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\
        \x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F\
        \x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2A\x2B\x2C\x2D\x2E\x2F\
        \x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3A\x3B\x3C\x3D\x3E\x3F\
        \x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4A\x4B\x4C\x4D\x4E\x4F\
        \x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5A\x5B\x5C\x5D\x5E\x5F\
        \x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6A\x6B\x6C\x6D\x6E\x6F\
        \x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7A\x7B\x7C\x7D\x7E\x7F\
        \x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F\
        \x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F\
        \xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF\
        \xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF\
        \xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\
    ";
    let mut output = [0u8; 64];
    let name = b"";
    let custom = b"Email Signature";
    let expected = b"\
        \x07\xDC\x27\xB1\x1E\x51\xFB\xAC\x75\xBC\x7B\x3C\x1D\x98\x3E\x8B\
        \x4B\x85\xFB\x1D\xEF\xAF\x21\x89\x12\xAC\x86\x43\x02\x73\x09\x17\
        \x27\xF4\x2B\x17\xED\x1D\xF6\x3E\x8E\xC1\x18\xF0\x4B\x23\x63\x3C\
        \x1D\xFB\x15\x74\xC8\xFB\x55\xCB\x45\xDA\x8E\x25\xAF\xB0\x92\xBB\
    ";
    let mut cshake = CShake::v256(name, custom);
    cshake.update(input);
    cshake.finalize(&mut output);
    assert_eq!(expected as &[u8], &output as &[u8]);
}

#[test]
fn test_cshake_as_shake() {
    let mut shake = CShake::v128(&[], &[]);
    let mut output = [0; 32];
    let expected = b"\
        \x43\xE4\x1B\x45\xA6\x53\xF2\xA5\xC4\x49\x2C\x1A\xDD\x54\x45\x12\
        \xDD\xA2\x52\x98\x33\x46\x2B\x71\xA4\x1A\x45\xBE\x97\x29\x0B\x6F\
    ";

    for _ in 0..16 {
        shake.squeeze(&mut output);
    }

    assert_eq!(expected, &output);
}
