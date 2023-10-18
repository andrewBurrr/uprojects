import { styled, Grid } from "@mui/material";

const FormGrid = styled(Grid) `
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: ${props => props.theme.spacing(2,6)};
` as typeof Grid;

export { FormGrid };