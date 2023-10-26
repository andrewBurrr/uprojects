import { styled, Button } from '@mui/material';

const FormButton = styled(Button) `
  border-radius: ${props => props.theme.shape.borderRadius};
  margin-top: ${props => props.theme.spacing(3)};
  margin-bottom: ${props => props.theme.spacing(2)};
` as typeof Button;

export { FormButton };