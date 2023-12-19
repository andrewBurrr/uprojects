import React from 'react';
import { Box, Card, Grid, Rating, styled, Typography} from "@mui/material";
import StarIcon from '@mui/icons-material/Star';

const TestimonialsBox = styled(Box) `
  display: flex;
  flex-grow: 1;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  width: 100%;
`

const TestimonialGridItem = styled(Grid) `
  padding: ${props => props.theme.spacing(2)};
`

const TestimonialCard = styled(Card) `
  display: flex;
  align-items: center;
  padding: ${props => props.theme.spacing(4)};
`

const StatementTypography = styled(Typography) `
  line-height: 1.5;
  min-height: 4.5em; 
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
`

const Testimonials = () => {
    const reviews = [
        {
            id: 1,
            name: 'John Doe',
            statement: 'This product is super great. Very professional!',
            rating: 3,
            position: 'Giga Chad',
        },
        {
            id: 2,
            name: 'Jane Doe',
            statement: 'I was amazed at how revolutionary this suite of products is. Wow oh wow! Your Quote Here. This is a long comment that may get truncated if it\'s too long. Your Quote Here. This is a long comment that may get truncated if it\'s too long.',
            rating: 2,
            position: 'CEO',
        },
        {
            id: 3,
            name: 'Jack Doe',
            statement: 'Aaaaaahhhhhhhhhh',
            rating: 3.5,
            position: 'The real boss man',
        }
    ];
    return (
        <TestimonialsBox>
            <Grid container>
                {reviews.map((review) => (
                    <TestimonialGridItem item xs={12} md={4} key={review.id}>
                        <TestimonialCard>
                                <Grid container direction="column" alignItems="center" justifyContent="center">
                                    <TestimonialGridItem item >
                                        <StatementTypography variant="body1" align="center" justifyContent="center">
                                            {review.statement}
                                        </StatementTypography>
                                    </TestimonialGridItem>
                                    <Grid item>
                                        <Rating value={review.rating} precision={0.5}  emptyIcon={<StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />} readOnly size="small" />
                                    </Grid>
                                    <Grid item>
                                        <Typography variant="subtitle1" fontWeight="bold" align="center">
                                            {review.name}
                                        </Typography>
                                        <Typography variant="subtitle2" align="center" color="textSecondary">
                                            {review.position}
                                        </Typography>
                                    </Grid>
                                </Grid>
                        </TestimonialCard>
                    </TestimonialGridItem>
                ))}
            </Grid>
        </TestimonialsBox>
    );
}

export { Testimonials };