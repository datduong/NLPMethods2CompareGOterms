# This code prepares bigram matrix from the MEDLIBE Abstracts (Please read the read-me file before use!)
use IO::File;

my $r1 = IO::File->new("../../Extra/word_index.dat","r") or die "Can not open file to read from;\nRun '1.1.Bigrams_2_Sparse_4_R_preparation.pl' first!\n";
my $r2 = IO::File->new("../../Extra/Pre_Bigram_Matrix.dat","r") or die "Can not open file to read from;\nRun '1.1.Bigrams_2_Sparse_4_R_preparation.pl' first!\n";
my $r3 = IO::File->new("../../Extra/Pre_Bigram_Matrix.dat","r") or die "Can not open file to read from;\nRun '1.1.Bigrams_2_Sparse_4_R_preparation.pl' first!\n";
open(my $w, '>', "../../Matrices/First_Order_Matrix.mtrx") or die "Could not open file to write in\n";

my $j = 1;
my $sum;
my $dim;
while(<$r1>){
	chomp;
	if ($j == 1){
		$j++;
		$sum = $_;
		next;
	}
	
	@a = split " ";
	$dim = $a[1];
}

my $n = 0;	### By changing '0' to another number define the maximum number of co-occurrence hepping for dimentionality reduction
while(<$r2>){
	chomp;
	my @b = split " ";
	if ($b[2] <= $n){ $sum = $sum - $b[2]; }
}

$w->print("%%MatrixMarket matrix coordinate real general\n"); ### This line is only for R (For MATLAB usage comment this out)
$w->print("$dim $dim $sum\n");

while(<$r3>){
	chomp;
	my @a = split " ";
	if ($a[2] > $n){
		$w->print("$_\n");
	}
}
