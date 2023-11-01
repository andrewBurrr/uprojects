import { styled, TextField } from '@mui/material';

const FormTextField = styled(TextField) `
  border-radius: ${props => props.theme.shape.borderRadius};
` as typeof TextField;

export { FormTextField };